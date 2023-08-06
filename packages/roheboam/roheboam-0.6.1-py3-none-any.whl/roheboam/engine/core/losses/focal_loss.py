from torch.nn import functional as F

from . import BaseLoss


class FocalLoss(BaseLoss):
    def __init__(self, name=None, gamma=2, multilabel=False, per_sample_loss_aggregate_method="SUM"):
        super().__init__(name)
        self.gamma = gamma
        self.multilabel = multilabel
        self.per_sample_loss_aggregate_method = per_sample_loss_aggregate_method

    # def to_call_kwargs(self, d):
    #     predictions = d["predictions"]
    #     targets = d["targets"]
    #     auxillary = d["auxillary"]

    #     method_args = {"predictions": d["predictions"]}

    #     if auxillary is not None and "weight_maps" in d["auxillary"]:
    #         method_args["weight_maps"] = d["auxillary"]["weight_maps"]["data"]

    #     if "masks" in d["targets"]:
    #         method_args["targets"] = d["targets"]["masks"]["data"]
    #         return method_args

    #     if "labels" in d["targets"]:
    #         method_args["targets"] = d["targets"]["labels"]["data"]
    #         return method_args

    #     raise MissingMethodArgumentException(
    #         f"There must be a 'd['targets']['labels'] or 'd['targets']['masks']
    #            key defined in the keys\n: {d['targets'].keys()}\nprovided by the dictionary"
    #     )

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

    def __call__(self, predictions, targets, auxillary={}):
        # This returns B x ... (same shape as input)
        weight_maps = auxillary.get("weight_maps")
        if weight_maps is not None:
            self._unreduced_loss = weight_maps * focal_loss(predictions, targets, self.gamma)
        else:
            self._unreduced_loss = focal_loss(predictions, targets, self.gamma)

        self._per_sample_loss = self.reshape_to_batch_size_x_minus_one_aggregate_over_last_dimension(
            self._unreduced_loss, aggregate_method=self.per_sample_loss_aggregate_method
        )
        self._reduced_loss = self._per_sample_loss.mean()
        self._total_loss = self._reduced_loss
        return self._total_loss


class CrossEntropyLoss(FocalLoss):
    def __init__(self, name=None, multilabel=False, per_sample_loss_aggregate_method="SUM"):
        super().__init__(name, gamma=0, multilabel=multilabel, per_sample_loss_aggregate_method=per_sample_loss_aggregate_method)


def focal_loss(input, target, gamma=2, multilabel=False):
    """

    :param input: B x N_classes x ...
    :param target: B x N_classes x ... # one hot encoding
    :param gamma: the higher the value, the greater the loss for uncertain classes
    :return:
    """

    if not (target.size() == input.size()):
        target = F.one_hot(target, num_classes=input.size(-1))

    target = target.float()

    if multilabel:
        max_val = (-input).clamp(min=0)
        loss = input - input * target + max_val + ((-max_val).exp() + (-input - max_val).exp()).log()
        inv_probs = F.logsigmoid(-input * (target * 2.0 - 1.0))
        loss = (inv_probs * gamma).exp() * loss
    else:
        loss = -1.0 * F.log_softmax(input, dim=-1) * target
    return loss
