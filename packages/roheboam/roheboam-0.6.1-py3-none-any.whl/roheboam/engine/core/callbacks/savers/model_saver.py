from enum import Enum
from pathlib import Path

import torch

from ..callback import Callback
from ..handler import CallbackHandlerContextValues


class ModelSaver(Callback):
    def __init__(
        self, save_directory=None, save_frequency="IMPROVEMENT", save_condition="LESSER", monitor_value="VALIDATION_LOSS", config=None, name=None
    ):
        assert save_frequency in ["EVERY", "IMPROVEMENT"]
        assert save_condition in ["LESSER", "GREATER"]
        super().__init__(name)
        self.config = config
        self.save_directory = save_directory
        self.previous_monitor_value = None
        self.save_frequency = save_frequency
        self.save_condition = save_condition
        self.monitor_value = CallbackHandlerContextValues[monitor_value]

    def on_train_epoch_end(self, context):
        self.current_monitor_value = self._get_monitor_value(context)
        if (
            (context.current_epoch == 0)
            or (self.save_frequency == "EVERY")
            or (self.save_frequency == "IMPROVEMENT" and self._is_better_than_previous_monitor_value())
        ):

            self._save(context)
            self.previous_monitor_value = self._get_monitor_value(context)

    def _save(self, context):
        model = context.model
        save_directory = self._construct_save_directory(context)
        model_save_path = self._save_model(save_directory, model)
        self._save_configuration(save_directory, model_save_path)

    def _construct_save_directory(self, context):
        return self.save_directory if self.save_directory is not None else context.save_directory

    def _save_model(self, save_directory, model):
        save_directory.mkdir(parents=True, exist_ok=True)
        model_save_path = save_directory / "model.p"
        torch.save(model.state_dict(), model_save_path)
        return model_save_path

    def _save_configuration(self, save_directory, model_save_path):
        self.config.model_save_path = model_save_path
        self.config.dump_config_to_path(Path(save_directory) / "config.yml")

    def _is_better_than_previous_monitor_value(self):
        if self.save_condition == "LESSER":
            return self.current_monitor_value < self.previous_monitor_value
        if self.save_condition == "GREATER":
            return self.current_monitor_value > self.previous_monitor_value

    def _get_monitor_value(self, context):
        return context[self.monitor_value]
