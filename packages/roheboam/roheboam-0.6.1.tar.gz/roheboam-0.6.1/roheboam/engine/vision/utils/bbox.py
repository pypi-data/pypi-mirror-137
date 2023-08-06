import math
import sys
from copy import deepcopy

import numpy as np
import torch
from torchvision.ops import nms as torchvision_nms

from ...utils.convenience import to_numpy


def clip_bboxes(bboxes, height, width):
    """[summary]
    :param bboxes: x, y, w, h, or x1, y1, x2, y2
    :type bboxes: [type]
    """
    bboxes[:, 0] = np.clip(bboxes[:, 0], 0, width - sys.float_info.epsilon)
    bboxes[:, 1] = np.clip(bboxes[:, 1], 0, height - sys.float_info.epsilon)
    bboxes[:, 2] = np.clip(bboxes[:, 2], 0, width - sys.float_info.epsilon)
    bboxes[:, 3] = np.clip(bboxes[:, 3], 0, height - sys.float_info.epsilon)
    return bboxes


def denormalize_bboxes_for_image(bboxes, height, width):
    if len(bboxes) == 0:
        return bboxes

    bboxes = deepcopy(bboxes)
    bboxes[:, 0] *= width
    bboxes[:, 1] *= height
    bboxes[:, 2] *= width
    bboxes[:, 3] *= height

    return bboxes


def normalize_bboxes_for_image(bboxes, height, width):
    if len(bboxes) == 0:
        return bboxes

    bboxes = deepcopy(bboxes)
    bboxes[:, 0] /= width
    bboxes[:, 1] /= height
    bboxes[:, 2] /= width
    bboxes[:, 3] /= height
    return bboxes


def xyxy_to_cxcywh(x):
    if len(x) == 0:
        return x

    # Convert nx4 boxes from [x1, y1, x2, y2] to [center_x, center_y, w, h] where xy1=top-left, xy2=bottom-right
    y = torch.zeros_like(x) if isinstance(x, torch.Tensor) else np.zeros_like(x)
    y[:, 0] = (x[:, 0] + x[:, 2]) / 2  # x center
    y[:, 1] = (x[:, 1] + x[:, 3]) / 2  # y center
    y[:, 2] = x[:, 2] - x[:, 0]  # width
    y[:, 3] = x[:, 3] - x[:, 1]  # height
    return y


def cxcywh_to_xyxy(x):
    if len(x) == 0:
        return x

    # Convert nx4 boxes from [center_x, center_y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = torch.zeros_like(x) if isinstance(x, torch.Tensor) else np.zeros_like(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2  # top left x
    y[:, 1] = x[:, 1] - x[:, 3] / 2  # top left y
    y[:, 2] = x[:, 0] + x[:, 2] / 2  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3] / 2  # bottom right y
    return y


def xywh_to_xyxy(x):
    if len(x) == 0:
        return x

    # Convert nx4 boxes from [x, y, w, h] to [x1, y1, x2, y2] where xy1=top-left, xy2=bottom-right
    y = torch.zeros_like(x) if isinstance(x, torch.Tensor) else np.zeros_like(x)
    y[:, 0] = x[:, 0]  # top left x
    y[:, 1] = x[:, 1]  # top left y
    y[:, 2] = x[:, 0] + x[:, 2]  # bottom right x
    y[:, 3] = x[:, 1] + x[:, 3]  # bottom right y
    return y


def bboxes_to_tensor(bboxes, scale_fn=None, format_fn=None):
    bboxes = deepcopy(bboxes)

    if scale_fn is not None:
        bboxes = scale_fn(bboxes)

    if format_fn is not None:
        bboxes = format_fn(bboxes)

    bboxes = torch.from_numpy(bboxes)

    return bboxes


def tensor_to_bboxes(tensor, unscale_fn=None, format_fn=None):
    bboxes = to_numpy(tensor)

    if format_fn is not None:
        bboxes = format_fn(bboxes)

    if unscale_fn is not None:
        bboxes = unscale_fn(bboxes)

    return bboxes


def iou_xywh_numpy(boxes1, boxes2):
    """
    :param boxes1: boxes1和boxes2的shape可以不相同，但是需要满足广播机制
    :param boxes2: 且需要保证最后一维为坐标维，以及坐标的存储结构为(x,y,w,h)，其中(x,y)是bbox的中心坐标
    :return: 返回boxes1和boxes2的IOU，IOU的shape为boxes1和boxes2广播后的shape[:-1]
    """
    boxes1 = np.array(boxes1)
    boxes2 = np.array(boxes2)

    boxes1_area = boxes1[..., 2] * boxes1[..., 3]
    boxes2_area = boxes2[..., 2] * boxes2[..., 3]

    # 分别计算出boxes1和boxes2的左上角坐标、右下角坐标
    # 存储结构为(xmin, ymin, xmax, ymax)，其中(xmin,ymin)是bbox的左上角坐标，(xmax,ymax)是bbox的右下角坐标
    boxes1 = np.concatenate([boxes1[..., :2] - boxes1[..., 2:] * 0.5, boxes1[..., :2] + boxes1[..., 2:] * 0.5], axis=-1)
    boxes2 = np.concatenate([boxes2[..., :2] - boxes2[..., 2:] * 0.5, boxes2[..., :2] + boxes2[..., 2:] * 0.5], axis=-1)

    # 计算出boxes1与boxes1相交部分的左上角坐标、右下角坐标
    left_up = np.maximum(boxes1[..., :2], boxes2[..., :2])
    right_down = np.minimum(boxes1[..., 2:], boxes2[..., 2:])

    # 因为两个boxes没有交集时，(right_down - left_up) < 0，所以maximum可以保证当两个boxes没有交集时，它们之间的iou为0
    inter_section = np.maximum(right_down - left_up, 0.0)
    inter_area = inter_section[..., 0] * inter_section[..., 1]
    union_area = boxes1_area + boxes2_area - inter_area
    IOU = 1.0 * inter_area / union_area
    return IOU


def ciou_xywh_torch(boxes1, boxes2):
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


def convert_bbox_yolo_to_pascal(bboxes, image):
    height, width, _ = image.shape
    return cxcywh_to_xyxy(denormalize_bboxes_for_image(bboxes, height=height, width=width))


def nms_with_scores(boxes, scores, labels, iou_threshold=0.1):
    boxes = torch.from_numpy(boxes) if isinstance(boxes, np.ndarray) else boxes
    scores = torch.from_numpy(scores) if isinstance(scores, np.ndarray) else scores
    labels = torch.from_numpy(labels) if isinstance(labels, np.ndarray) else labels
    nms_idxs = torchvision_nms(boxes, scores, iou_threshold)
    return {"boxes": boxes[nms_idxs], "scores": scores[nms_idxs], "labels": labels[nms_idxs]}


lookup = {
    "bboxes_to_tensor": bboxes_to_tensor,
    "ciou_xywh_torch": ciou_xywh_torch,
    "clip_bboxes": clip_bboxes,
    "convert_bbox_yolo_to_pascal": convert_bbox_yolo_to_pascal,
    "denormalize_bboxes_for_image": denormalize_bboxes_for_image,
    "iou_xywh_numpy": iou_xywh_numpy,
    "normalize_bboxes_for_image": normalize_bboxes_for_image,
    "xyxy_to_cxcywh": xyxy_to_cxcywh,
    "tensor_to_bboxes": tensor_to_bboxes,
    "cxcywh_to_xyxy": cxcywh_to_xyxy,
    "cxcywh_to_xyxy": cxcywh_to_xyxy,
    "nms_with_scores": nms_with_scores,
}
