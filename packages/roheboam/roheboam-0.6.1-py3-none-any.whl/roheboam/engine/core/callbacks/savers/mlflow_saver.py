from pathlib import Path

import cloudpickle
import mlflow
from pytorch_lightning.utilities import rank_zero_only

from ....utils.conda import get_current_conda_env
from ....utils.saving import save_to_temporary_file
from .. import Callback


class MLflowModelSaver(Callback):
    def __init__(self, config, lookup, pipeline, mlflow_model, root_save_path, conda_env_name=None, lookup_save_name="lookup.p"):
        self.config = config
        self.lookup = lookup
        self.lookup_save_name = lookup_save_name
        self.mlflow_model = mlflow_model
        self.mlflow_model_save_path = Path(root_save_path) / "mlflow"
        self.conda_env_name = conda_env_name

    def save_lookup(self, file_name):
        cloudpickle.dump(self.lookup, open(file_name, "wb"))

    @rank_zero_only
    def on_teardown(self, context):
        with save_to_temporary_file(self.save_lookup, self.lookup_save_name) as lookup_file_path:
            conda_env = get_current_conda_env(env_name=self.conda_env_name)
            artifacts = {
                "config_path": str(self.config.save_path),
                "model_save_path": str(self.config.model_save_path),
                "lookup_path": str(lookup_file_path),
            }
            mlflow.pyfunc.save_model(path=self.mlflow_model_save_path, python_model=self.mlflow_model, artifacts=artifacts, conda_env=conda_env)
