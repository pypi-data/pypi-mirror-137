import pytorch_lightning as pl

from ....core.callbacks import CallbackHandler, CallbackHandlerContextValues
from ....utils.convenience import debug_log_on_call


class PytorchLightningCallbacksToCallbackHandlerAdapter(pl.Callback):
    def __init__(self, callback_handler: CallbackHandler):
        self.callback_handler = callback_handler

    @debug_log_on_call
    def setup(self, trainer, model, stage):
        """Called in the beginning of fit and test"""
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TRAINER, trainer)
        self.callback_handler.on_setup()

    @debug_log_on_call
    def teardown(self, trainer, model, stage):
        """Called at the end of fit and test"""
        self.callback_handler.on_teardown()

    @debug_log_on_call
    def on_init_start(self, trainer):
        """Called when the trainer initialization begins, model has not yet been set."""
        self.callback_handler.on_init_begin()

    @debug_log_on_call
    def on_init_end(self, trainer):
        """Called when the trainer initialization ends, model has not yet been set."""
        self.callback_handler.on_init_end()

    @debug_log_on_call
    def on_fit_start(self, trainer, model):
        """Called when the trainer initialization begins, model has not yet been set."""
        pass

    @debug_log_on_call
    def on_fit_end(self, trainer, model):
        """Called when the trainer initialization begins, model has not yet been set."""
        pass

    def on_sanity_check_start(self, trainer, model):
        """Called when the validation sanity check starts."""
        pass

    def on_sanity_check_end(self, trainer, model):
        """Called when the validation sanity check ends."""
        pass

    def on_train_epoch_start(self, trainer, model):
        """Called when the epoch begins."""
        self.callback_handler.set_context_value(CallbackHandlerContextValues.CURRENT_EPOCH, trainer.current_epoch)
        self.callback_handler.on_train_epoch_begin()

    def on_train_epoch_end(self, trainer, model):
        """Called when the epoch ends."""
        pass

    def on_validation_epoch_start(self, trainer, model):
        """Called when the epoch begins."""
        self.callback_handler.on_validation_epoch_begin()

    def on_validation_epoch_end(self, trainer, model):
        """Called when the epoch ends."""
        pass

    def on_test_epoch_start(self, trainer, model):
        """Called when the epoch begins."""
        self.callback_handler.on_test_epoch_begin()
        pass

    def on_test_epoch_end(self, trainer, model):
        """Called when the epoch ends."""
        pass

    def on_epoch_start(self, trainer, model):
        """Called when the epoch begins."""
        pass

    def on_epoch_end(self, trainer, model):
        """Called when the epoch ends."""
        pass

    def on_train_start(self, trainer, model):
        """Called when the train begins."""
        self.callback_handler.set_context_value(CallbackHandlerContextValues.MODEL, model)
        self.callback_handler.on_train_begin()

    def on_train_end(self, trainer, model):
        """Called when the train ends."""
        self.callback_handler.on_train_end()
        pass

    def on_pretrain_routine_start(self, trainer, model):
        """Called when the train begins."""
        pass

    def on_pretrain_routine_end(self, trainer, model):
        """Called when the train ends."""
        pass

    def on_batch_start(self, trainer, model):
        """Called when the training batch begins."""
        pass

    def on_batch_end(self, trainer, model):
        """Called when the training batch ends."""
        pass

    def on_train_batch_start(self, trainer, model, batch, batch_idx, dataloader_idx):
        """Called when the training batch begins."""
        self.callback_handler.set_context_value(CallbackHandlerContextValues.CURRENT_STEP, trainer.global_step)
        pass

    def on_train_batch_end(self, trainer, model, outputs, batch, batch_idx, dataloader_idx):
        """Called when the training batch ends."""
        self.callback_handler.on_train_batch_end()

    def on_validation_batch_start(self, trainer, model, batch, batch_idx, dataloader_idx):
        """Called when the validation batch begins."""
        self.callback_handler.set_context_value(CallbackHandlerContextValues.CURRENT_STEP, trainer.global_step)
        pass

    def on_validation_batch_end(self, trainer, model, outputs, batch, batch_idx, dataloader_idx):
        """Called when the validation batch ends."""
        self.callback_handler.on_validation_batch_end()

    def on_test_batch_start(self, trainer, model, batch, batch_idx, dataloader_idx):
        self.callback_handler.set_context_value(CallbackHandlerContextValues.CURRENT_STEP, trainer.global_step)
        """Called when the test batch begins."""
        pass

    def on_test_batch_end(self, trainer, model, outputs, batch, batch_idx, dataloader_idx):
        """Called when the test batch ends."""
        self.callback_handler.on_test_batch_end()

    def on_validation_start(self, trainer, model):
        """Called when the validation loop begins."""
        self.callback_handler.set_context_value(CallbackHandlerContextValues.MODEL, model)
        self.callback_handler.on_validation_begin()

    def on_validation_end(self, trainer, model):
        """Called when the validation loop ends."""
        self.callback_handler.on_validation_end()

    def on_test_start(self, trainer, model):
        """Called when the test begins."""
        self.callback_handler.set_context_value(CallbackHandlerContextValues.MODEL, model)
        self.callback_handler.on_test_begin()

    def on_test_end(self, trainer, model):
        """Called when the test ends."""
        self.callback_handler.on_test_end()

    def on_keyboard_interrupt(self, trainer, model):
        """Called when the training is interrupted by KeyboardInterrupt."""
        pass


lookup = {"PytorchLightningCallbacksToCallbackHandlerAdapter": PytorchLightningCallbacksToCallbackHandlerAdapter}
