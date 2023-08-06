import numpy as np


class LabelStatisticsForMeanAveragePrecision:
    def __init__(self, label):
        self.label = label
        self.false_positives = []
        self.true_positives = []
        self.scores = []
        self.num_annotations = 0

    @property
    def true_positives_sorted_by_confidence_cumulative_sum(self):
        true_positives_sorted_by_confidence = np.array(self.true_positives)[np.argsort(-np.array(self.scores))]
        true_positives_sorted_by_confidence_cumulative_sum = np.cumsum(true_positives_sorted_by_confidence)
        return true_positives_sorted_by_confidence_cumulative_sum

    @property
    def false_positives_sorted_by_confidence_cumulative_sum(self):
        false_positives_sorted_by_confidence = np.array(self.false_positives)[np.argsort(-np.array(self.scores))]
        false_positives_sorted_by_confidence_cumulative_sum = np.cumsum(false_positives_sorted_by_confidence)
        return false_positives_sorted_by_confidence_cumulative_sum

    @property
    def recall(self):
        return self.true_positives_sorted_by_confidence_cumulative_sum / self.num_annotations

    @property
    def precision(self):
        return self.true_positives_sorted_by_confidence_cumulative_sum / np.maximum(
            self.true_positives_sorted_by_confidence_cumulative_sum + self.false_positives_sorted_by_confidence_cumulative_sum,
            np.finfo(np.float64).eps,
        )

    @property
    def average_precision(self):
        return self._compute_ap(self.recall, self.precision)

    def _compute_ap(self, recall, precision):
        """Compute the average precision, given the recall and precision curves.
        Code originally from https://github.com/rbgirshick/py-faster-rcnn.
        # Arguments
            recall:    The recall curve (list).
            precision: The precision curve (list).
        # Returns
            The average precision as computed in py-faster-rcnn.
        """
        # correct AP calculation
        # first append sentinel values at the end
        mrec = np.concatenate(([0.0], recall, [1.0]))
        mpre = np.concatenate(([0.0], precision, [0.0]))

        # compute the precision envelope
        for i in range(mpre.size - 1, 0, -1):
            mpre[i - 1] = np.maximum(mpre[i - 1], mpre[i])

        # to calculate area under PR curve, look for points
        # where X axis (recall) changes value
        i = np.where(mrec[1:] != mrec[:-1])[0]

        # and sum (\Delta recall) * prec
        ap = np.sum((mrec[i + 1] - mrec[i]) * mpre[i + 1])
        return ap


lookup = {"LabelStatisticsForMeanAveragePrecision": LabelStatisticsForMeanAveragePrecision}
