import pytorch_lightning as pl

from ......core.callbacks import CallbackHandlerContextValues
from ......utils.convenience import debug_log_on_call, timing, to_numpy


class _LightningModuleMeta(type):
    def __instancecheck__(self, other):
        return type(other) == pl.LightningModule


class PytorchLightningImageClassificationModule(pl.LightningModule, metaclass=_LightningModuleMeta):
    @debug_log_on_call
    def __init__(
        self,
        model_creator,
        optimizer_creator,
        train_samples,
        train_dataset_creator,
        train_dataloader_creator,
        loss,
        val_samples=None,
        val_dataset_creator=None,
        val_dataloader_creator=None,
        test_samples=None,
        test_dataset_creator=None,
        test_dataloader_creator=None,
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.model = model_creator()
        self.optimizer_creator = optimizer_creator
        self.loss = loss

        self.train_samples = train_samples
        self.train_dataset_creator = train_dataset_creator
        self.train_dataloader_creator = train_dataloader_creator

        self.val_samples = val_samples
        self.val_dataset_creator = val_dataset_creator
        self.val_dataloader_creator = val_dataloader_creator

        self.test_samples = test_samples
        self.test_dataset_creator = test_dataset_creator
        self.test_dataloader_creator = test_dataloader_creator

    @debug_log_on_call
    def _can_train(self):
        return self.train_samples is not None and self.train_dataset_creator is not None and self.train_dataloader_creator is not None

    @debug_log_on_call
    def _can_val(self):
        return self.val_samples is not None and self.val_dataset_creator is not None and self.val_dataloader_creator is not None

    @debug_log_on_call
    def _can_test(self):
        return self.test_samples is not None and self.test_dataset_creator is not None and self.test_dataloader_creator is not None

    @debug_log_on_call
    def prepare_data(self):
        if self._can_train():
            self.train_dataset = self.train_dataset_creator(samples_data=self.train_samples)
        if self._can_val():
            self.val_dataset = self.val_dataset_creator(samples_data=self.val_samples)
        if self._can_test():
            self.test_dataset = self.test_dataset_creator(samples_data=self.test_samples)

    @debug_log_on_call
    def train_dataloader(self):
        return self.train_dataloader_creator(self.train_dataset)

    @debug_log_on_call
    def val_dataloader(self):
        if self._can_val():
            return self.val_dataloader_creator(self.val_dataset)
        else:
            return None

    @debug_log_on_call
    def test_dataloader(self):
        if self._can_test():
            return self.test_dataloader_creator(self.test_dataset)
        else:
            return None

    @debug_log_on_call
    def configure_optimizers(self):
        return self.optimizer_creator(self.model.parameters())

    @debug_log_on_call
    def training_step(self, batch, batch_idx):
        x = batch["images"]
        y = batch["labels"]
        prediction = self(x)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TRAIN_PREDICTION, prediction)
        prediction = self.callback_handler.on_train_loss_begin()
        loss = self.loss(prediction, y)
        return {"loss": loss}

    @debug_log_on_call
    def forward(self, x):
        return self.model(x)

    @debug_log_on_call
    def validation_step(self, batch, batch_idx):
        x = batch["images"]
        y = batch["labels"]
        prediction = self.model(x)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.VALIDATION_PREDICTION, prediction)
        prediction = self.callback_handler.on_validation_loss_begin()
        loss = self.loss(prediction, y)
        return {"val_loss": loss}

    @debug_log_on_call
    def test_step(self, batch, batch_idx):
        x = batch["images"]
        prediction = self.model(x)

        output = {"prediction": to_numpy(prediction)}
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TEST_PREDICTION, prediction)
        prediction = self.callback_handler.on_test_loss_begin()

        if "labels" in batch:
            y = batch["labels"]
            loss = self.loss(prediction, y)
            output.update({"test_loss": loss})
        return output


def create_pytorch_lightning_image_classification_module(
    callback_handler,
    model_creator,
    optimizer_creator=None,
    loss=None,
    train_samples=None,
    train_dataset_creator=None,
    train_dataloader_creator=None,
    val_samples=None,
    val_dataset_creator=None,
    val_dataloader_creator=None,
    test_samples=None,
    test_dataset_creator=None,
    test_dataloader_creator=None,
):
    from ......integrations.pytorch_lightning.adapters import PytorchLightningModuleHooksToCallbackHandlerAdapter

    return PytorchLightningModuleHooksToCallbackHandlerAdapter(
        PytorchLightningImageClassificationModule(
            model_creator=model_creator,
            optimizer_creator=optimizer_creator,
            loss=loss,
            train_samples=train_samples,
            train_dataset_creator=train_dataset_creator,
            train_dataloader_creator=train_dataloader_creator,
            val_samples=val_samples,
            val_dataset_creator=val_dataset_creator,
            val_dataloader_creator=val_dataloader_creator,
            test_samples=test_samples,
            test_dataset_creator=test_dataset_creator,
            test_dataloader_creator=test_dataloader_creator,
        ),
        callback_handler,
    )


lookup = {
    "PytorchLightningImageClassificationModule": PytorchLightningImageClassificationModule,
    "create_pytorch_lightning_image_classification_module": create_pytorch_lightning_image_classification_module,
}
