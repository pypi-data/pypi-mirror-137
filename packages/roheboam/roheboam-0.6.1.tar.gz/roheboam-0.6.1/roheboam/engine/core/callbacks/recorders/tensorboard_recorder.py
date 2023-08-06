from pathlib import Path

from torch.utils.tensorboard import SummaryWriter

from ....logger import logger
from ....utils.convenience import catch_all_exceptions
from .. import Callback


class TensorboardRecorder(Callback):
    _order = -10

    def __init__(self, root_save_path, name=None):
        super().__init__(name)
        self.tensorboard_save_path = Path(root_save_path) / "tensorboard"
        self._writer = None

    def getWriter(self):
        if self._writer is None:
            self._writer = SummaryWriter(log_dir=self.tensorboard_save_path)
            logger.info(f"Run tensorboard --logdir {str(self.tensorboard_save_path)}")
        return self._writer

    def on_train_batch_end(self, context):
        self._record_loss(context.loss, context.current_phase, context.current_step)

    def on_validation_epoch_begin(self, context):
        self.validation_step_offset = 0

    def on_validation_batch_end(self, context):
        self._record_loss(context.loss, context.current_phase, context.current_step + self.validation_step_offset)
        self.validation_step_offset += 1

    def on_validation_epoch_end(self, context):
        self._record_metric_on_epoch_end(context.validation_metric, context.current_phase, context.current_step + self.validation_step_offset)

    def on_test_batch_end(self, context):
        self._record_loss(context.loss, context.current_phase, context.current_step)

    def on_test_epoch_end(self, context):
        self._record_metric_on_epoch_end(context.test_metric, context.current_phase, context.current_step)

    def _record_loss(self, losses, phase, step):
        phase = str(phase)
        all_losses = {"Total": losses.total_loss.item()}
        for loss_name, loss_value in losses.reduced_losses.items():
            key = f"{phase}/{loss_name}"
            loss = loss_value.item()
            self.getWriter().add_scalar(key, loss, step)
            all_losses[key] = loss
        self.getWriter().add_scalars(f"{str(phase)}/All Losses", all_losses, step)

    def _record_metric_on_epoch_end(self, metrics, phase, step):
        if metrics is None:
            return

        for metric in metrics.metrics:
            metric.write_to_tensorboard_on_epoch_end(self.getWriter(), phase, step)
