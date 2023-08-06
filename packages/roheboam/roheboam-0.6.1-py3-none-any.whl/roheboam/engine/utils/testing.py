from copy import deepcopy

import numpy as np


def all_methods_in_callback_handler_are_called(callback_handler):
    return all(callback_handler.get_callback_by_name("CallbackMethodIsCalled").method_is_called.values())


def arrays_are_same(array1, array2):
    return np.all(array1 == array2)


def copy_and_flatten_model_weights(model):
    return deepcopy([p.cpu().detach().numpy().flatten() for p in model.parameters()])


lookup = {
    "all_methods_in_callback_handler_are_called": all_methods_in_callback_handler_are_called,
    "arrays_are_same": arrays_are_same,
    "copy_and_flatten_model_weights": copy_and_flatten_model_weights,
}
