from . import BaseLoss


class TorchVisionFasterRCNNLoss(BaseLoss):
    def __init__(self, loss_key, name=None):
        super().__init__(name)
        self.loss_key = loss_key

    def to_call_kwargs(self, d):
        return {"loss": d["predictions"][self.loss_key]}

    @property
    def unreduced_loss(self):
        return self.loss

    @property
    def per_sample_loss(self):
        return self.loss

    @property
    def reduced_loss(self):
        return self.loss

    @property
    def total_loss(self):
        return self.loss

    def __call__(self, loss):
        self.loss = loss
        return loss
