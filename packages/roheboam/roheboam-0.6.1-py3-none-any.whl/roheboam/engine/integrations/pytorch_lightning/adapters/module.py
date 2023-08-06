import pytorch_lightning as pl

from roheboam.engine.utils.convenience import timing

from ....core.callbacks import CallbackHandlerContextValues
from ....utils.convenience import debug_log_on_call


class LightningModuleWrapper:
    def __init__(self, lightning_module):
        self.lightning_module = lightning_module

    def __getattr__(self, name):
        return getattr(self.lightning_module, name)

    def __setattr__(self, name, value):
        if name == "lightning_module":
            super().__setattr__(name, value)
        else:
            setattr(self.lightning_module, name, value)


class PytorchLightningModuleHooksToCallbackHandlerAdapter(pl.LightningModule):
    """
    This wraps the LightningModule to inject the hooks by wrapping the LightningModule hooks.

    training_step:
        on_train_batch_begin
        on_train_loss_begin

    validation_step:
        on_validation_batch_begin
        on_validation_loss_begin

    test_step:
        on_test_batch_begin
        on_test_loss_begin
    """

    # def __class__(cls):
    #     return pl.LightningModule

    @debug_log_on_call
    def __init__(self, lightning_module, callback_handler):
        lightning_module.callback_handler = callback_handler

        self.callback_handler = callback_handler
        self.lightning_module = LightningModuleWrapper(lightning_module)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.LOSS, self.lightning_module.loss)

    def __setattr__(self, name, value):
        if name in ["callback_handler", "lightning_module"]:
            super().__setattr__(name, value)
        else:
            setattr(self.lightning_module, name, value)

    def __getattr__(self, name):
        if name in ["callback_handler", "lightning_module"]:
            return super().__getattr__(name)
        else:
            return getattr(self.lightning_module, name)

    @debug_log_on_call
    def prepare_data(self):
        self.lightning_module.prepare_data()

    @debug_log_on_call
    def train_dataloader(self):
        return self.lightning_module.train_dataloader()

    @debug_log_on_call
    def val_dataloader(self):
        return self.lightning_module.val_dataloader()

    @debug_log_on_call
    def test_dataloader(self):
        return self.lightning_module.test_dataloader()

    @debug_log_on_call
    def configure_optimizers(self):
        return self.lightning_module.configure_optimizers()

    @debug_log_on_call
    def training_step(self, batch, batch_idx):
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TRAIN_BATCH, batch)
        batch = self.callback_handler.on_train_batch_begin()
        loss = self.lightning_module.training_step(batch, batch_idx)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TRAIN_LOSS, loss.get("loss"))
        return loss

    @debug_log_on_call
    def forward(self, x):
        return self.lightning_module.forward(x)

    @debug_log_on_call
    def training_step_end(self, outputs):
        module_outputs = self.lightning_module.training_step_end(outputs)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TRAIN_OUTPUT, outputs if module_outputs is None else module_outputs)
        outputs = self.callback_handler.on_train_step_end()
        return outputs

    @debug_log_on_call
    def backward(self, loss, optimizer, optimizer_idx):
        loss = self.callback_handler.on_backward_begin()
        self.lightning_module.backward(loss, optimizer, optimizer_idx)

    @debug_log_on_call
    def on_after_backward(self):
        self.lightning_module.on_after_backward()
        self.callback_handler.on_backward_end()

    @debug_log_on_call
    def validation_step(self, batch, batch_idx):
        self.callback_handler.set_context_value(CallbackHandlerContextValues.VALIDATION_BATCH, batch)
        batch = self.callback_handler.on_validation_batch_begin()
        loss = self.lightning_module.validation_step(batch, batch_idx)

        self.callback_handler.set_context_value(CallbackHandlerContextValues.VALIDATION_LOSS, loss.get("val_loss"))
        return loss

    @debug_log_on_call
    def validation_step_end(self, outputs):
        module_outputs = self.lightning_module.validation_step_end(outputs)
        self.callback_handler.set_context_value(
            CallbackHandlerContextValues.VALIDATION_OUTPUT, outputs if module_outputs is None else module_outputs
        )
        outputs = self.callback_handler.on_validation_step_end()
        return outputs

    @debug_log_on_call
    def validation_epoch_end(self, outputs):
        module_outputs = self.lightning_module.validation_epoch_end(outputs)
        self.callback_handler.set_context_value(
            CallbackHandlerContextValues.ALL_VALIDATION_OUTPUT, outputs if module_outputs is None else module_outputs
        )
        all_outputs = self.callback_handler.on_validation_epoch_end()
        return all_outputs

    @debug_log_on_call
    def training_epoch_end(self, outputs):
        module_outputs = self.lightning_module.training_epoch_end(outputs)
        self.callback_handler.set_context_value(
            CallbackHandlerContextValues.ALL_TRAIN_OUTPUT, outputs if module_outputs is None else module_outputs
        )
        self.callback_handler.on_train_epoch_end()

    @debug_log_on_call
    def test_step(self, batch, batch_idx):
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TEST_BATCH, batch)
        batch = self.callback_handler.on_test_batch_begin()
        loss = self.lightning_module.test_step(batch, batch_idx)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TEST_LOSS, loss.get("test_loss"))
        return loss

    @debug_log_on_call
    def test_step_end(self, outputs):
        module_outputs = self.lightning_module.test_step_end(outputs)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TEST_OUTPUT, outputs if module_outputs is None else module_outputs)
        outputs = self.callback_handler.on_test_step_end()
        return outputs

    @debug_log_on_call
    def test_epoch_end(self, outputs):
        module_outputs = self.lightning_module.test_epoch_end(outputs)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.ALL_TEST_OUTPUT, outputs if module_outputs is None else module_outputs)
        all_outputs = self.callback_handler.on_test_epoch_end()
        return all_outputs


lookup = {"PytorchLightningModuleHooksToCallbackHandlerAdapter": PytorchLightningModuleHooksToCallbackHandlerAdapter}
