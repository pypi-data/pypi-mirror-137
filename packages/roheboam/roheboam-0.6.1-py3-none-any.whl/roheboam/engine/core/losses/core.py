from abc import abstractmethod

import numpy as np

from ...utils.convenience import camel2snake
from ...utils.interfaces import MapDictionaryToMethodArguments


class LossWrapper:
    def __init__(self, losses):
        super().__init__()
        for loss in losses:
            setattr(self, camel2snake(loss.__class__.__name__), loss)
        self.losses = losses

    def __call__(self, predictions, targets={}, auxillary={}):
        total_loss = 0
        for loss in self.losses:
            loss_args = loss.to_call_kwargs(dict(predictions=predictions, targets=targets, auxillary=auxillary))
            total_loss += loss(**loss_args).float()
        return total_loss

    @property
    def reduced_losses(self):
        losses = {}
        for loss in self.losses:
            try:
                per_batch_losses = loss.reduced_loss
                if isinstance(per_batch_losses, dict):
                    losses.update(loss.reduced_loss)
                else:
                    losses[loss.name] = loss.reduced_loss
            except AttributeError:
                losses[loss.name] = np.array([None])
        return losses

    @property
    def per_sample_losses(self):
        losses = {}
        for loss in self.losses:
            try:
                per_sample_loss = loss.per_sample_loss
                if isinstance(per_sample_loss, dict):
                    losses.update(loss.per_sample_loss)
                else:
                    losses[loss.name] = loss.per_sample_loss
            except AttributeError:
                losses[loss.name] = np.array([None])
        return losses

    @property
    def total_loss(self):
        return sum([loss.total_loss for loss in self.losses])


class BaseLoss(MapDictionaryToMethodArguments):
    loss_name_incrementor = 0

    def __init__(self, name):
        if name is None:
            self.name = f"{self.__class__.__name__}-{BaseLoss.loss_name_incrementor}"
            BaseLoss.loss_name_incrementor += 1
        else:
            self.name = name

    def to_call_kwargs(self, d):
        return d

    @staticmethod
    def reshape_to_batch_size_x_minus_one_and_sum_over_last_dimension(tensor):
        return BaseLoss.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(tensor, aggregate_method="SUM")

    @staticmethod
    def reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(tensor, aggregate_method="SUM"):
        batch_size = tensor.size(0)
        if aggregate_method == "SUM":
            return tensor.view(batch_size, -1).sum(dim=1)
        elif aggregate_method == "MEAN":
            return tensor.view(batch_size, -1).mean(dim=1)
        else:
            raise KeyError("Aggregation method not found")

    @property
    @abstractmethod
    def unreduced_loss(self):
        pass

    @property
    @abstractmethod
    def per_sample_loss(self):
        pass

    @property
    @abstractmethod
    def reduced_loss(self):
        pass
