import mlflow


def load_mlflow_pyfunc_model(model_save_path):
    from ....engine import get_toolbox_lookup

    model_save_path = str(model_save_path)
    model = mlflow.pyfunc.load_model(model_save_path)
    python_model = model._model_impl.python_model
    python_model.lookup = get_toolbox_lookup()
    python_model.preload_context(model._model_impl.context)
    return model


lookup = {"load_mlflow_pyfunc_model": load_mlflow_pyfunc_model}
