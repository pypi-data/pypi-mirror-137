from torchvision.ops import box_iou as torchvision_box_iou

from ...utils.training import tensorify
from .core import BaseMetric


class BoxIOU(BaseMetric):
    def __init__(self, threshold=0.5, name=None):
        super().__init__(name)
        self.threshold = threshold

    @property
    def unreduced_metric(self):
        return self._unreduced_metric

    @property
    def per_sample_metric(self):
        return self.metric

    @property
    def reduced_metric(self):
        return self.metric

    @property
    def total_metric(self):
        return self.metric

    def to_call_kwargs(self, d):
        predicted_boxes = d["predictions"]["boxes"]
        predicted_labels = d["predictions"]["labels"]
        predicted_scores = d["predictions"]["scores"]
        target_boxes = d["targets"]["boxes"]
        target_labels = d["targets"]["labels"]
        return {
            "predicted_boxes": predicted_boxes,
            "predicted_labels": predicted_labels,
            "predicted_scores": predicted_scores,
            "target_boxes": target_boxes,
            "target_labels": target_labels,
        }

    def __call__(self, predicted_boxes, predicted_labels, predicted_scores, target_boxes, target_labels):

        self._unreduced_metric = box_iou(predicted_boxes, target_boxes)
        self._per_sample_metric = self._unreduced_metric.diag()
        self._reduced_metric = self._per_sample_metric.mean()
        self._total_metric = self._reduced_metric
        return self._total_metric


def box_iou(predictions, targets):
    """Return intersection-over-union (Jaccard index) of boxes.

    Args:
        prediction (N, 4): ground truth boxes.
        target (N, 4): predicted boxes.
        eps: a small number to avoid 0 as denominator.
    Returns:
        iou (N): IoU values.
    """
    return torchvision_box_iou(tensorify(predictions).float(), tensorify(targets).float())


lookup = {"BoxIOU": BoxIOU, "box_iou": box_iou}
