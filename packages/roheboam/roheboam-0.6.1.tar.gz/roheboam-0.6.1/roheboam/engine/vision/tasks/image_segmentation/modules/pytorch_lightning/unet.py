import pytorch_lightning as pl

from ......core.callbacks import CallbackHandlerContextValues
from ......utils.convenience import debug_log_on_call


class PytorchLightningUNet(pl.LightningModule):
    @debug_log_on_call
    def __init__(
        self,
        model_creator,
        optimizer_creator,
        loss,
        train_samples,
        train_dataset_creator,
        train_dataloader_creator,
        scheduler_creator=None,
        val_samples=None,
        val_dataset_creator=None,
        val_dataloader_creator=None,
        test_samples=None,
        test_dataset_creator=None,
        test_dataloader_creator=None,
    ):
        super().__init__()
        self.model = model_creator()
        self.optimizer_creator = optimizer_creator
        self.scheduler_creator = scheduler_creator
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
        self.train_dataset = self.train_dataset_creator(self.train_samples)
        if self._can_val():
            self.val_dataset = self.val_dataset_creator(self.val_samples)
        if self._can_test():
            self.test_dataset = self.test_dataset_creator(self.test_samples)

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
        self.optimizer = self.optimizer_creator(filter(lambda p: p.requires_grad, self.model.parameters()))
        if self.scheduler_creator is None:
            return self.optimizer

        self.scheduler = self.scheduler_creator(self.optimizer)

        return self.optimizer, [{"scheduler": self.scheduler}]

    @debug_log_on_call
    def training_step(self, batch, batch_idx):
        images = batch["images"]
        masks = batch["masks"]
        predictions = self(images)
        loss = self.loss(predictions, masks)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TRAIN_PREDICTION, predictions)
        predictions = self.callback_handler.on_train_loss_begin()
        return {"prediction": predictions.cpu().detach().numpy(), "loss": loss}

    @debug_log_on_call
    def forward(self, x):
        return self.model(x)

    @debug_log_on_call
    def backward(self, loss, optimizer, optimizer_idx, *args, **kwargs):
        loss.backward(*args, **kwargs)

    @debug_log_on_call
    def validation_step(self, batch, batch_idx):
        images = batch["images"]
        masks = batch["masks"]
        predictions = self(images)
        loss = self.loss(predictions, masks)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.VALIDATION_PREDICTION, predictions)
        predictions = self.callback_handler.on_validation_loss_begin()
        return {"prediction": predictions.cpu().detach().numpy(), "val_loss": loss}

    @debug_log_on_call
    def test_step(self, batch, batch_idx):
        output = dict()
        images = batch["images"]
        predictions = self(images)

        self.callback_handler.set_context_value(CallbackHandlerContextValues.TEST_PREDICTION, predictions)

        predictions = self.callback_handler.on_test_loss_begin()
        output = {"prediction": predictions.cpu().detach().numpy()}

        if "masks" in batch:
            masks = batch["masks"]
            loss = self.loss(predictions, masks)
            output.update({"test_loss": loss})
        return output


def create_pytorch_lightning_unet_module(
    callback_handler,
    model_creator,
    optimizer_creator=None,
    loss=None,
    train_samples=None,
    train_dataset_creator=None,
    train_dataloader_creator=None,
    scheduler_creator=None,
    val_samples=None,
    val_dataset_creator=None,
    val_dataloader_creator=None,
    test_samples=None,
    test_dataset_creator=None,
    test_dataloader_creator=None,
):
    from ......integrations.pytorch_lightning import PytorchLightningModuleHooksToCallbackHandlerAdapter

    return PytorchLightningModuleHooksToCallbackHandlerAdapter(
        PytorchLightningUNet(
            model_creator=model_creator,
            optimizer_creator=optimizer_creator,
            loss=loss,
            train_samples=train_samples,
            train_dataset_creator=train_dataset_creator,
            train_dataloader_creator=train_dataloader_creator,
            scheduler_creator=scheduler_creator,
            val_samples=val_samples,
            val_dataset_creator=val_dataset_creator,
            val_dataloader_creator=val_dataloader_creator,
            test_samples=test_samples,
            test_dataset_creator=test_dataset_creator,
            test_dataloader_creator=test_dataloader_creator,
        ),
        callback_handler,
    )


lookup = {"create_pytorch_lightning_unet_module": create_pytorch_lightning_unet_module, "PytorchLightningUNet": PytorchLightningUNet}
