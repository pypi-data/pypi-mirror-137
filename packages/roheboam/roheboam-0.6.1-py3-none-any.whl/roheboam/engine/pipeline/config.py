from .config_loader import dump_config_to_path
from .constants import VARIABLE_KEY


class Configuration:
    def __init__(self, raw_config):
        self.raw_config = raw_config

    @property
    def variables(self):
        return self.raw_config[VARIABLE_KEY]

    @property
    def model_save_path(self):
        return self.raw_config[VARIABLE_KEY]["model_save_path"]

    @model_save_path.setter
    def model_save_path(self, path):
        self.raw_config[VARIABLE_KEY]["model_save_path"] = str(path)

    @property
    def root_save_directory(self):
        return self.raw_config[VARIABLE_KEY]["root_save_directory"]

    @root_save_directory.setter
    def root_save_directory(self, path):
        self.raw_config[VARIABLE_KEY]["root_save_directory"] = str(path)

    def dump_config_to_path(self, path):
        dump_config_to_path(self.raw_config, path)
