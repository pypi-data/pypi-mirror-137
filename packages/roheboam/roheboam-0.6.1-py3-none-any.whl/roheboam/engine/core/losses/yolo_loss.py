import math

import torch
import torch.nn as nn

from . import BaseLoss


class YOLOv4Loss(BaseLoss):
    def __init__(self, strides, iou_threshold_loss=0.5, name=None):
        super().__init__(name)
        self.strides = strides
        self.iou_threshold_loss = iou_threshold_loss

    def to_call_kwargs(self, d):
        return {**d["predictions"], **d["targets"]}

    @property
    def unreduced_loss(self):
        return self._unreduced_loss

    @property
    def per_sample_loss(self):
        return self._per_sample_loss

    @property
    def reduced_loss(self):
        return self._reduced_loss

    @property
    def total_loss(self):
        return self._total_loss

    def __call__(
        self,
        predictions,
        predictions_decoded,
        label_and_bboxes_small,
        label_and_bboxes_medium,
        label_and_bboxes_large,
        small_bboxes,
        medium_bboxes,
        large_bboxes,
    ):
        loss_small_ciou, loss_small_conf, loss_small_cls = yolo_v4_loss(
            predictions[0], predictions_decoded[0], label_and_bboxes_small, small_bboxes, self.strides[0], self.iou_threshold_loss, reduce=False
        )

        loss_medium_ciou, loss_medium_conf, loss_medium_cls = yolo_v4_loss(
            predictions[1], predictions_decoded[1], label_and_bboxes_medium, medium_bboxes, self.strides[1], self.iou_threshold_loss, reduce=False
        )

        loss_large_ciou, loss_large_conf, loss_large_cls = yolo_v4_loss(
            predictions[2], predictions_decoded[2], label_and_bboxes_large, large_bboxes, self.strides[2], self.iou_threshold_loss, reduce=False
        )

        self._unreduced_loss = {
            f"{self.name}_loss_small_ciou": loss_small_ciou,
            f"{self.name}_loss_small_conf": loss_small_conf,
            f"{self.name}_loss_small_cls": loss_small_cls,
            f"{self.name}_loss_medium_ciou": loss_medium_ciou,
            f"{self.name}_loss_medium_conf": loss_medium_conf,
            f"{self.name}_loss_medium_cls": loss_medium_cls,
            f"{self.name}_loss_large_ciou": loss_large_ciou,
            f"{self.name}_loss_large_conf": loss_large_conf,
            f"{self.name}_loss_large_cls": loss_large_cls,
        }

        self._per_sample_loss = {
            f"{self.name}_loss_small_ciou": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_small_ciou),
            f"{self.name}_loss_small_conf": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_small_conf),
            f"{self.name}_loss_small_cls": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_small_cls),
            f"{self.name}_loss_medium_ciou": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_medium_ciou),
            f"{self.name}_loss_medium_conf": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_medium_conf),
            f"{self.name}_loss_medium_cls": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_medium_cls),
            f"{self.name}_loss_large_ciou": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_large_ciou),
            f"{self.name}_loss_large_conf": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_large_conf),
            f"{self.name}_loss_large_cls": self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(loss_large_cls),
        }

        self._reduced_loss = {loss_name: loss_values.mean() for loss_name, loss_values in self.per_sample_loss.items()}

        self._total_loss = torch.stack(list(self._reduced_loss.values())).sum()

        return self._total_loss


def yolo_v4_loss(p, p_d, label, bboxes, stride, iou_threshold_loss, reduce=True):
    """
    label is BS x G x G x N_ANCHOR x ([x,y,w,h,c] + N_CLASSES)
    bboxes is BS x 150 x 4
    (1)The loss of regression of boxes.
        GIOU loss is defined in  https://arxiv.org/abs/1902.09630.

    Note: The loss factor is 2-w*h/(img_size**2), which is used to influence the
            balance of the loss value at different scales.
    (2)The loss of confidence.
        Includes confidence loss values for foreground and background.

    Note: The backgroud loss is calculated when the maximum iou of the box predicted
            by the feature point and all GTs is less than the threshold.
    (3)The loss of classes。
        The category loss is BCE, which is the binary value of each class.

    :param stride: The scale of the feature map relative to the original image

    :return: The average loss(loss_giou, loss_conf, loss_cls) of all batches of this detection layer.
    """
    BCE = nn.BCEWithLogitsLoss(reduction="none")
    FOCAL = FocalLoss(gamma=2, alpha=1.0, reduction="none")

    batch_size, grid = p.shape[:2]
    img_size = stride * grid

    p_conf = p[..., 4:5]
    p_cls = p[..., 5:]

    p_d_xywh = p_d[..., :4]

    label_xywh = label[..., :4]
    label_obj_mask = label[..., 4:5]
    label_cls = label[..., 5:]
    #         label_mix = label[..., 5:6]

    # loss ciou, p_d_xywh are the anchors, label_xywh are the labels for the anchors,
    # usually they are [0, 0, 0, 0] if the anchor doesn't have an object associated with it
    ciou = CIOU_xywh_torch(p_d_xywh, label_xywh).unsqueeze(-1)

    # The scaled weight of bbox is used to balance the impact of small objects and large objects on loss.
    bbox_loss_scale = 2.0 - 1.0 * label_xywh[..., 2:3] * label_xywh[..., 3:4] / (img_size ** 2)
    loss_ciou = label_obj_mask * bbox_loss_scale * (1.0 - ciou)

    # loss confidence
    iou = CIOU_xywh_torch(p_d_xywh.unsqueeze(4), bboxes.unsqueeze(1).unsqueeze(1).unsqueeze(1))
    iou_max = iou.max(-1, keepdim=True)[0]
    label_noobj_mask = (1.0 - label_obj_mask) * (iou_max < iou_threshold_loss).float()

    loss_conf = label_obj_mask * FOCAL(input=p_conf, target=label_obj_mask) + label_noobj_mask * FOCAL(input=p_conf, target=label_obj_mask)

    # loss classes
    loss_cls = label_obj_mask * BCE(input=p_cls, target=label_cls)

    loss_ciou_reduced = (torch.sum(loss_ciou)) / batch_size
    loss_conf_reduced = (torch.sum(loss_conf)) / batch_size
    loss_cls_reduced = (torch.sum(loss_cls)) / batch_size
    loss_reduced = loss_ciou + loss_conf + loss_cls

    if reduce:
        return loss_reduced, loss_ciou_reduced, loss_conf_reduced, loss_cls_reduced
    else:
        # BS x grid_size x grid_size x n_anchors_at_scale x 1 for loss_ciou & loss_conf
        # BS x grid_size x grid_size x n_anchors_at_scale x n_classes for loss_cls
        return loss_ciou, loss_conf, loss_cls


class _YOLOv4Loss(nn.Module):
    def __init__(self, strides, iou_threshold_loss=0.5):
        super().__init__()
        self.__iou_threshold_loss = iou_threshold_loss
        self.__strides = strides

    def forward(
        self,
        predictions,
        predictions_decoded,
        label_and_bboxes_small,
        label_and_bboxes_medium,
        label_and_bboxes_large,
        small_bboxes,
        medium_bboxes,
        large_bboxes,
    ):
        """
        :param p: Predicted offset values for three detection layers.
                    The shape is [p0, p1, p2], ex. p0=[bs, grid, grid, anchors, tx+ty+tw+th+conf+cls_20]
        :param p_d: Decodeed predicted value. The size of value is for image size.
                    ex. p_d0=[bs, grid, grid, anchors, x+y+w+h+conf+cls_20]
        :param label_sbbox: Small detection layer's label. The size of value is for original image size.
                    shape is [bs, grid, grid, anchors, x+y+w+h+conf+mix+cls_20]
        :param label_mbbox: Same as label_sbbox.
        :param label_lbbox: Same as label_sbbox.
        :param sbboxes: Small detection layer bboxes.The size of value is for original image size.
                        shape is [bs, 150, x+y+w+h]
        :param mbboxes: Same as sbboxes.
        :param lbboxes: Same as sbboxes
        """
        strides = self.__strides
        loss_small_ciou, loss_small_conf, loss_small_cls = self.__cal_loss_per_layer(
            predictions[0], predictions_decoded[0], label_and_bboxes_small, small_bboxes, strides[0], reduce=False
        )
        loss_medium_ciou, loss_medium_conf, loss_medium_cls = self.__cal_loss_per_layer(
            predictions[1], predictions_decoded[1], label_and_bboxes_medium, medium_bboxes, strides[1], reduce=False
        )
        loss_large_ciou, loss_large_conf, loss_large_cls = self.__cal_loss_per_layer(
            predictions[2], predictions_decoded[2], label_and_bboxes_large, large_bboxes, strides[2], reduce=False
        )

        return (
            [loss_small_ciou, loss_small_conf, loss_small_cls],
            [loss_medium_ciou, loss_medium_conf, loss_medium_cls],
            [loss_large_ciou, loss_large_conf, loss_large_cls],
        )

    def __cal_loss_per_layer(self, p, p_d, label, bboxes, stride, reduce=True):
        """
        label is BS x G x G x N_ANCHOR x ([x,y,w,h,c] + N_CLASSES)
        bboxes is BS x 150 x 4
        (1)The loss of regression of boxes.
          GIOU loss is defined in  https://arxiv.org/abs/1902.09630.

        Note: The loss factor is 2-w*h/(img_size**2), which is used to influence the
             balance of the loss value at different scales.
        (2)The loss of confidence.
            Includes confidence loss values for foreground and background.

        Note: The backgroud loss is calculated when the maximum iou of the box predicted
              by the feature point and all GTs is less than the threshold.
        (3)The loss of classes。
            The category loss is BCE, which is the binary value of each class.

        :param stride: The scale of the feature map relative to the original image

        :return: The average loss(loss_giou, loss_conf, loss_cls) of all batches of this detection layer.
        """
        BCE = nn.BCEWithLogitsLoss(reduction="none")
        FOCAL = FocalLoss(gamma=2, alpha=1.0, reduction="none")

        batch_size, grid = p.shape[:2]
        img_size = stride * grid

        p_conf = p[..., 4:5]
        p_cls = p[..., 5:]

        p_d_xywh = p_d[..., :4]

        label_xywh = label[..., :4]
        label_obj_mask = label[..., 4:5]
        label_cls = label[..., 5:]
        #         label_mix = label[..., 5:6]

        # loss ciou, p_d_xywh are the anchors, label_xywh are the labels for the anchors, usually they are [0, 0, 0, 0]
        # if the anchor doesn't have an object associated with it
        ciou = CIOU_xywh_torch(p_d_xywh, label_xywh).unsqueeze(-1)

        # The scaled weight of bbox is used to balance the impact of small objects and large objects on loss.
        bbox_loss_scale = 2.0 - 1.0 * label_xywh[..., 2:3] * label_xywh[..., 3:4] / (img_size ** 2)
        loss_ciou = label_obj_mask * bbox_loss_scale * (1.0 - ciou)

        # loss confidence
        iou = CIOU_xywh_torch(p_d_xywh.unsqueeze(4), bboxes.unsqueeze(1).unsqueeze(1).unsqueeze(1))
        iou_max = iou.max(-1, keepdim=True)[0]
        label_noobj_mask = (1.0 - label_obj_mask) * (iou_max < self.__iou_threshold_loss).float()

        loss_conf = label_obj_mask * FOCAL(input=p_conf, target=label_obj_mask) + label_noobj_mask * FOCAL(input=p_conf, target=label_obj_mask)

        # loss classes
        loss_cls = label_obj_mask * BCE(input=p_cls, target=label_cls)

        loss_ciou_reduced = (torch.sum(loss_ciou)) / batch_size
        loss_conf_reduced = (torch.sum(loss_conf)) / batch_size
        loss_cls_reduced = (torch.sum(loss_cls)) / batch_size
        loss_reduced = loss_ciou + loss_conf + loss_cls

        if reduce:
            return loss_reduced, loss_ciou_reduced, loss_conf_reduced, loss_cls_reduced
        else:
            # BS x grid_size x grid_size x n_anchors_at_scale x 1 for loss_ciou & loss_conf
            # BS x grid_size x grid_size x n_anchors_at_scale x n_classes for loss_cls
            return loss_ciou, loss_conf, loss_cls


class FocalLoss(nn.Module):
    def __init__(self, gamma=2.0, alpha=1.0, reduction="mean"):
        super(FocalLoss, self).__init__()
        self.__gamma = gamma
        self.__alpha = alpha
        self.__loss = nn.BCEWithLogitsLoss(reduction=reduction)

    def forward(self, input, target):
        loss = self.__loss(input=input, target=target)
        loss *= self.__alpha * torch.pow(torch.abs(target - torch.sigmoid(input)), self.__gamma)

        return loss


def CIOU_xywh_torch(boxes1, boxes2):
    """
    cal CIOU of two boxes or batch boxes
    :param boxes1:[xmin,ymin,xmax,ymax] or
                [[xmin,ymin,xmax,ymax],[xmin,ymin,xmax,ymax],...]
    :param boxes2:[xmin,ymin,xmax,ymax]
    :return:
    """
    # xywh->xyxy
    boxes1 = torch.cat([boxes1[..., :2] - boxes1[..., 2:] * 0.5, boxes1[..., :2] + boxes1[..., 2:] * 0.5], dim=-1)
    boxes2 = torch.cat([boxes2[..., :2] - boxes2[..., 2:] * 0.5, boxes2[..., :2] + boxes2[..., 2:] * 0.5], dim=-1)

    boxes1 = torch.cat([torch.min(boxes1[..., :2], boxes1[..., 2:]), torch.max(boxes1[..., :2], boxes1[..., 2:])], dim=-1)
    boxes2 = torch.cat([torch.min(boxes2[..., :2], boxes2[..., 2:]), torch.max(boxes2[..., :2], boxes2[..., 2:])], dim=-1)

    boxes1_area = (boxes1[..., 2] - boxes1[..., 0]) * (boxes1[..., 3] - boxes1[..., 1])
    boxes2_area = (boxes2[..., 2] - boxes2[..., 0]) * (boxes2[..., 3] - boxes2[..., 1])

    inter_left_up = torch.max(boxes1[..., :2], boxes2[..., :2])
    inter_right_down = torch.min(boxes1[..., 2:], boxes2[..., 2:])
    inter_section = torch.max(inter_right_down - inter_left_up, torch.zeros_like(inter_right_down))
    inter_area = inter_section[..., 0] * inter_section[..., 1]
    union_area = boxes1_area + boxes2_area - inter_area
    ious = 1.0 * inter_area / union_area

    # cal outer boxes
    outer_left_up = torch.min(boxes1[..., :2], boxes2[..., :2])
    outer_right_down = torch.max(boxes1[..., 2:], boxes2[..., 2:])
    outer = torch.max(outer_right_down - outer_left_up, torch.zeros_like(inter_right_down))
    outer_diagonal_line = torch.pow(outer[..., 0], 2) + torch.pow(outer[..., 1], 2)

    # cal center distance
    boxes1_center = (boxes1[..., :2] + boxes1[..., 2:]) * 0.5
    boxes2_center = (boxes2[..., :2] + boxes2[..., 2:]) * 0.5
    center_dis = torch.pow(boxes1_center[..., 0] - boxes2_center[..., 0], 2) + torch.pow(boxes1_center[..., 1] - boxes2_center[..., 1], 2)

    # cal penalty term
    # cal width,height
    boxes1_size = torch.max(boxes1[..., 2:] - boxes1[..., :2], torch.zeros_like(inter_right_down))
    boxes2_size = torch.max(boxes2[..., 2:] - boxes2[..., :2], torch.zeros_like(inter_right_down))
    v = (4 / (math.pi ** 2)) * torch.pow(
        torch.atan((boxes1_size[..., 0] / torch.clamp(boxes1_size[..., 1], min=1e-6)))
        - torch.atan((boxes2_size[..., 0] / torch.clamp(boxes2_size[..., 1], min=1e-6))),
        2,
    )
    alpha = v / (1 - ious + v)

    # cal ciou
    cious = ious - (center_dis / outer_diagonal_line + alpha * v)

    return cious
