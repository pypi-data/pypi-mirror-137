import mlflow

from ...utils.conda import get_current_conda_env


def save_mlflow_pyfunc_model(model_save_path, model, artifacts=None, conda_env_name=None):
    model_save_path = str(model_save_path)
    conda_env = get_current_conda_env(env_name=conda_env_name)
    mlflow.pyfunc.save_model(path=model_save_path, python_model=model, artifacts=artifacts, conda_env=conda_env)


lookup = {"save_mlflow_pyfunc_model": save_mlflow_pyfunc_model}
