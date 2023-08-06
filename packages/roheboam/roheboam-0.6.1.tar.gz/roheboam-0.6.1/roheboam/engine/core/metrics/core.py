from abc import abstractmethod

import numpy as np

from ...utils.convenience import camel2snake
from ...utils.interfaces import TransformToCallKeywordArguments


class MetricWrapper:
    def __init__(self, metrics):
        super().__init__()
        for metric in metrics:
            setattr(self, camel2snake(metric.__class__.__name__), metric)
        self.metrics = metrics

    def __call__(self, predictions, targets={}, auxillary={}):
        all_metrics = []
        for metric in self.metrics:
            metric_args = metric.transform_to_kwargs(predictions=predictions, targets=targets, auxillary=auxillary)
            all_metrics.append(metric(**metric_args))
        return all_metrics


class BaseMetric(TransformToCallKeywordArguments):
    metric_name_incrementor = 0

    def __init__(self, name):
        if name is None:
            self.name = f"{self.__class__.__name__}-{BaseMetric.metric_name_incrementor}"
            BaseMetric.metric_name_incrementor += 1
        else:
            self.name = name


lookup = {"MetricWrapper": MetricWrapper}
