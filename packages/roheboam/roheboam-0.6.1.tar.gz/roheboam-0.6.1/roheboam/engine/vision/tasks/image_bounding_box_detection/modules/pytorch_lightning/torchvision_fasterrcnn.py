import pytorch_lightning as pl

from ......core.callbacks import CallbackHandlerContextValues
from ......utils.convenience import debug_log_on_call


class PytorchLightningTorchVisionFasterRCNN(pl.LightningModule):
    @debug_log_on_call
    def __init__(
        self,
        model_creator,
        optimizer_creator,
        loss,
        metric=None,
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
        *args,
        **kwargs
    ):
        super().__init__(*args, **kwargs)
        self.model = model_creator()
        self.optimizer_creator = optimizer_creator
        self.scheduler_creator = scheduler_creator
        self.loss = loss
        self.metric = metric

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
        if self.scheduler_creator is not None:
            self.scheduler = self.scheduler_creator(self.optimizer)
            return [self.optimizer, [{"scheduler": self.scheduler}]]
        return self.optimizer

    @debug_log_on_call
    def training_step(self, batch, batch_idx):
        images = batch["images"]
        targets = batch["targets"]
        losses = self.model.forward(images, targets)
        loss = self.loss(predictions=losses)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TRAIN_PREDICTION, losses)

        losses = self.callback_handler.on_train_loss_begin()

        return {"loss": loss}

    @debug_log_on_call
    def forward(self, x):
        return self.model.forward(x)

    @debug_log_on_call
    def backward(self, loss, optimizer, optimizer_idx, *args, **kwargs):
        loss.backward(*args, **kwargs)

    @debug_log_on_call
    def validation_step(self, batch, batch_idx):
        images = batch["images"]
        targets = batch["targets"]
        self.model.train()

        losses = self.model.forward(images, targets)
        loss = self.loss(predictions=losses)
        self.model.eval()

        predictions = self.model.forward(images)
        if self.metric is not None:
            self.metric(predictions, targets)
            self.callback_handler.set_context_value(CallbackHandlerContextValues.VALIDATION_METRIC, self.metric)
        self.callback_handler.set_context_value(CallbackHandlerContextValues.VALIDATION_PREDICTION, predictions)
        predictions = self.callback_handler.on_validation_loss_begin()
        return {"val_loss": loss}

    @debug_log_on_call
    def test_step(self, batch, batch_idx):
        images = batch["images"]
        predictions = self.model.forward(images)
        output = {"prediction": predictions}
        self.callback_handler.set_context_value(CallbackHandlerContextValues.TEST_PREDICTION, predictions)
        predictions = self.callback_handler.on_test_loss_begin()
        if "targets" in batch:
            targets = batch["targets"]
            self.model.train()
            losses = self.model.forward(images, targets)
            self.model.eval()
            loss = self.loss(predictions=losses)
            output.update({"test_loss": loss})

        if "targets" in batch and self.metric is not None:
            self.metric(predictions, targets)
            self.callback_handler.set_context_value(CallbackHandlerContextValues.TEST_METRIC, self.metric)
        return output


def create_pytorch_lightning_torchvision_fasterrcnn(
    callback_handler,
    model_creator,
    optimizer_creator,
    loss,
    metric=None,
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
        PytorchLightningTorchVisionFasterRCNN(
            model_creator,
            optimizer_creator,
            loss,
            metric,
            train_samples,
            train_dataset_creator,
            train_dataloader_creator,
            scheduler_creator,
            val_samples,
            val_dataset_creator,
            val_dataloader_creator,
            test_samples,
            test_dataset_creator,
            test_dataloader_creator,
        ),
        callback_handler,
    )


lookup = {
    "create_pytorch_lightning_torchvision_fasterrcnn": create_pytorch_lightning_torchvision_fasterrcnn,
    "PytorchLightningTorchVisionFasterRCNN": PytorchLightningTorchVisionFasterRCNN,
}
