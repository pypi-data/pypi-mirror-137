import numpy as np

from ....utils.convenience import to_numpy
from ..core import BaseMetric
from .label_statistics import LabelStatisticsForMeanAveragePrecision


class _TensorboardMixin:
    def write_to_tensorboard_on_epoch_end(self, tensorboard_writer, phase, step):
        all_aps = {"mAP": self.mean_average_precision}

        for label in self.labels:
            key = f"{str(phase)}/AP for {label}"
            average_precision = self.average_precision_for_label(label)
            # tensorboard_writer.add_scalar(
            #     key,
            #     average_precision,
            #     step,
            # )
            all_aps[key] = average_precision

        tensorboard_writer.add_scalars(f"{str(phase)}/AP for all label NMS: {self.nms_threshold} IOU: {self.iou_threshold}", all_aps, step)

        self._create_label_statistics_dict()


def mean_average_precision_torchvision_fasterrcnn_transform_fn(predictions, targets, auxillary):
    return {
        "predicted_boxes": [to_numpy(prediction["boxes"]) for prediction in predictions],
        "predicted_labels": [to_numpy(prediction["labels"]) for prediction in predictions],
        "predicted_scores": [to_numpy(prediction["scores"]) for prediction in predictions],
        "target_boxes": [to_numpy(target["boxes"]) for target in targets],
        "target_labels": [to_numpy(target["labels"]) for target in targets],
    }


class MeanAveragePrecision(BaseMetric, _TensorboardMixin):
    def __init__(
        self,
        iou_threshold,
        nms_threshold=None,
        n_classes=None,
        labels=None,
        transform_to_kwargs_fn=mean_average_precision_torchvision_fasterrcnn_transform_fn,
        name=None,
    ):
        assert (n_classes is None) ^ (labels is None)
        super().__init__(name)
        self.nms_threshold = nms_threshold
        self.iou_threshold = iou_threshold
        self.transform_to_kwargs_fn = transform_to_kwargs_fn
        self._n_classes = n_classes
        self._labels = labels
        self._create_label_statistics_dict()

    def transform_to_kwargs(self, predictions, targets, auxillary):
        return self.transform_to_kwargs_fn(predictions, targets, auxillary)

    def _create_label_statistics_dict(self):
        if self._n_classes is not None:
            self.label_statistics_dict = {label: LabelStatisticsForMeanAveragePrecision(label) for label in range(self._n_classes)}

        if self._labels is not None:
            self.label_statistics_dict = {label: LabelStatisticsForMeanAveragePrecision(label) for label in self._labels}

    @property
    def labels(self):
        return list(self.label_statistics_dict.keys())

    @property
    def mean_average_precision(self):
        return np.mean([label_stats.average_precision for label_stats in self.label_statistics_dict.values() if label_stats.num_annotations > 0])

    def average_precision_for_label(self, label):
        return self.label_statistics_dict[label].average_precision

    def __call__(self, predicted_boxes, predicted_labels, predicted_scores, target_boxes, target_labels):
        for (
            predicted_boxes_for_sample,
            predicted_labels_for_sample,
            predicted_scores_for_sample,
            target_boxes_for_sample,
            target_labels_for_sample,
        ) in zip(predicted_boxes, predicted_labels, predicted_scores, target_boxes, target_labels):
            for label in self.label_statistics_dict.keys():
                (
                    predicted_boxes_for_label,
                    _,
                    scores_for_predicted_label,
                    target_boxes_for_label,
                    _,
                ) = self._create_predicted_and_targets_given_label(
                    label,
                    predicted_boxes_for_sample,
                    predicted_labels_for_sample,
                    predicted_scores_for_sample,
                    target_boxes_for_sample,
                    target_labels_for_sample,
                )

                self._update_statistics_for_label(label, predicted_boxes_for_label, scores_for_predicted_label, target_boxes_for_label)

    def _create_predicted_and_targets_given_label(self, label, predicted_boxes, predicted_labels, predicted_scores, target_boxes, target_labels):
        idxs_for_label_predicted = np.where(predicted_labels == label)[0]
        predicted_boxes_for_label = predicted_boxes[idxs_for_label_predicted]
        predicted_labels_for_label = predicted_labels[idxs_for_label_predicted]
        predicted_scores_for_label = predicted_scores[idxs_for_label_predicted]

        idxs_for_label_target = np.where(target_labels == label)[0]
        target_boxes_for_label = target_boxes[idxs_for_label_target]
        target_labels_for_label = target_labels[idxs_for_label_target]
        return (predicted_boxes_for_label, predicted_labels_for_label, predicted_scores_for_label, target_boxes_for_label, target_labels_for_label)

    def _update_statistics_for_label(self, label, predicted_boxes_for_label, scores_for_predicted_label, target_boxes_for_label):

        if len(predicted_boxes_for_label) == 0 and len(target_boxes_for_label) == 0:
            return

        self.label_statistics_dict[label].num_annotations += len(target_boxes_for_label)

        detected_annotations = []

        if self.nms_threshold is not None:
            idxs_to_keep = self._nms(predicted_boxes_for_label, scores_for_predicted_label, self.nms_threshold)
            predicted_boxes_for_label = predicted_boxes_for_label[idxs_to_keep]
            scores_for_predicted_label = scores_for_predicted_label[idxs_to_keep]

        for predicted_box_for_label, score in zip(predicted_boxes_for_label, scores_for_predicted_label):

            self.label_statistics_dict[label].scores.append(score)

            # If there are no annotations, but a box was predicted anyways, we found a false positive
            if len(target_boxes_for_label) == 0:
                self.label_statistics_dict[label].false_positives.append(1)
                self.label_statistics_dict[label].true_positives.append(0)
                continue

            # Find the predicted box that has the highest IoU with all the annotations
            overlaps = self._compute_overlap(np.expand_dims(predicted_box_for_label, axis=0), target_boxes_for_label)
            assigned_annotation = np.argmax(overlaps, axis=1)
            max_overlap = overlaps[0, assigned_annotation]

            # If the IoU of the detected box is greater than the threshold & it hasn't been used, we found a true position
            if max_overlap >= self.iou_threshold and assigned_annotation not in detected_annotations:
                self.label_statistics_dict[label].false_positives.append(0)
                self.label_statistics_dict[label].true_positives.append(1)
                detected_annotations.append(assigned_annotation)
            # Or else we found a false_positive
            else:
                self.label_statistics_dict[label].false_positives.append(1)
                self.label_statistics_dict[label].true_positives.append(0)

    # --------------------------------------------------------
    # Fast R-CNN
    # Copyright (c) 2015 Microsoft
    # Licensed under The MIT License [see LICENSE for details]
    # Written by Ross Girshick
    # --------------------------------------------------------
    def _nms(self, boxes, scores, threshold):
        """
        boxes is a numpy array: num_boxes, 4
        scores is a  numpy array: num_boxes
        """
        x1 = boxes[:, 0]
        y1 = boxes[:, 1]
        x2 = boxes[:, 2]
        y2 = boxes[:, 3]

        areas = (x2 - x1 + 1) * (y2 - y1 + 1)
        order = scores.argsort()[::-1]  # get boxes with more ious first

        keep = []
        while order.size > 0:
            i = order[0]  # pick maxmum iou box
            keep.append(i)
            xx1 = np.maximum(x1[i], x1[order[1:]])
            yy1 = np.maximum(y1[i], y1[order[1:]])
            xx2 = np.minimum(x2[i], x2[order[1:]])
            yy2 = np.minimum(y2[i], y2[order[1:]])

            w = np.maximum(0.0, xx2 - xx1 + 1)  # maximum width
            h = np.maximum(0.0, yy2 - yy1 + 1)  # maxiumum height
            inter = w * h
            ovr = inter / (areas[i] + areas[order[1:]] - inter)

            inds = np.where(ovr <= threshold)[0]
            order = order[inds + 1]

        return keep

    def _compute_overlap(self, boxes, query_boxes):
        """
        Args
            a: (N, 4) ndarray of float
            b: (K, 4) ndarray of float
        Returns
            overlaps: (N, K) ndarray of overlap between boxes and query_boxes
        """
        N = boxes.shape[0]
        K = query_boxes.shape[0]
        overlaps = np.zeros((N, K), dtype=np.float64)
        for k in range(K):
            box_area = (query_boxes[k, 2] - query_boxes[k, 0]) * (query_boxes[k, 3] - query_boxes[k, 1])
            for n in range(N):
                iw = min(boxes[n, 2], query_boxes[k, 2]) - max(boxes[n, 0], query_boxes[k, 0])
                if iw > 0:
                    ih = min(boxes[n, 3], query_boxes[k, 3]) - max(boxes[n, 1], query_boxes[k, 1])
                    if ih > 0:
                        ua = np.float64((boxes[n, 2] - boxes[n, 0]) * (boxes[n, 3] - boxes[n, 1]) + box_area - iw * ih)
                        overlaps[n, k] = iw * ih / ua
        return overlaps


lookup = {
    "MeanAveragePrecision": MeanAveragePrecision,
    "mean_average_precision_torchvision_fasterrcnn_transform_fn": mean_average_precision_torchvision_fasterrcnn_transform_fn,
}
