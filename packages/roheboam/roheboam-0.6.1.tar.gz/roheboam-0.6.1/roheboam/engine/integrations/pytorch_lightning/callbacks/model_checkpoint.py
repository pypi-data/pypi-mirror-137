from pathlib import Path

from pytorch_lightning.callbacks import ModelCheckpoint

from ....core.callbacks import Callback


class PyTorchLightningModelCheckpoint(Callback):
    def __init__(self, config, root_save_path):
        super().__init__()
        self.config = config
        self.model_save_path = Path(root_save_path) / "checkpoints"
        self.model_checkpoint = ModelCheckpoint(dirpath=str(self.model_save_path))

    @property
    def current_model_path(self):
        return self.model_save_path / self.current_model_save_name

    @property
    def best_model_path(self):
        return self.model_checkpoint.best_model_path

    @property
    def best_config_path(self):
        return f"{self.model_checkpoint.best_model_path}.config.yml"

    def on_validation_end(self, context):
        trainer = context.trainer
        epoch, step = trainer.current_epoch, trainer.global_step
        self.current_model_save_name = Path(self.format_checkpoint_name(epoch, step)).name
        self.model_save_path.mkdir(exist_ok=True, parents=True)
        self.model_checkpoint.save_checkpoint(trainer)
        self._save_configuration()

    def format_checkpoint_name(self, epoch, step):
        return str(self.model_save_path / f"epoch={epoch}-step={step}.ckpt")

    def _save_configuration(self):
        config_save_path = self.model_save_path / f"{self.current_model_save_name}.config.yml"
        self.config.model_save_path = str(self.model_save_path / self.current_model_save_name)
        self.config.save_path = config_save_path
        self.config.dump_config_to_path(config_save_path)

    def on_save_checkpoint(self, trainer_callback_hook_mixin, model):
        return None


lookup = {"PyTorchLightningModelCheckpoint": PyTorchLightningModelCheckpoint}
