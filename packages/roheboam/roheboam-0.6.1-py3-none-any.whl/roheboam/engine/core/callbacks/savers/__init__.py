from .mlflow_saver import MLflowModelSaver
from .model_saver import ModelSaver

lookup = {"ModelSaver": ModelSaver, "MLflowModelSaver": MLflowModelSaver}
