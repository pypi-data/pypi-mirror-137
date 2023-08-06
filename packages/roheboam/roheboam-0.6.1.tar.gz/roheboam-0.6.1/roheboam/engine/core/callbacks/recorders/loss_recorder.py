from ....utils.convenience import to_numpy
from .. import Callback
from .utils import Storage


class PerSampleLossRecorder(Callback):
    _order = -10

    def __init__(self, name=None):
        super().__init__(name)
        self.losses = Storage()

    def _store_losses(self, batch, loss, phase, epoch, step):
        for loss_name, loss_values in loss.per_sample_losses.items():
            detached_loss_values = to_numpy(loss_values).tolist()
            if not isinstance(detached_loss_values, list):
                detached_loss_values = [detached_loss_values]
            self.losses.write(str(phase), epoch, loss_name, detached_loss_values)

    def on_train_batch_end(self, context):
        self._store_losses(context.train_batch, context.loss, context.current_phase, context.current_epoch, context.current_step)

    def on_validation_batch_end(self, context):
        self._store_losses(context.validation_batch, context.loss, context.current_phase, context.current_epoch, context.current_step)

    def on_test_batch_end(self, context):
        self._store_losses(context.test_batch, context.loss, context.current_phase, context.current_epoch, context.current_step)
