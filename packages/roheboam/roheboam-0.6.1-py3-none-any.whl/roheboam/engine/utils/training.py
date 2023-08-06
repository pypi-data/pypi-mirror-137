import logging
import os
import re
import time
from enum import Enum

import numpy as np
import torch

from .convenience import if_none, is_listy


def num_cpus() -> int:
    try:
        return len(os.sched_getaffinity(0))
    except AttributeError:
        return os.cpu_count()


default_cpus = min(1, num_cpus())
default_device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")


# https://stackoverflow.com/questions/29831489/convert-array-of-indices-to-1-hot-encoded-numpy-array
def make_one_hot(x, n_classes=None, channel_first=False, dtype=np.float32):
    """1-hot encode x with the max value n (computed from data if n is None)."""
    x = np.asarray(x)
    n = np.max(x) + 1 if n_classes is None else n_classes
    one_hot = np.eye(n, dtype=dtype)[x]
    if not channel_first:
        return one_hot
    return one_hot.transpose(2, 0, 1)


def tensorify(lst):
    """
    List must be nested list of tensors (with no varying lengths within a dimension).
    Nested list of nested lengths [D1, D2, ... DN] -> tensor([D1, D2, ..., DN)

    :return: nested list D
    """
    # base case, if the current list is not nested anymore, make it into tensor
    if type(lst[0]) != list:
        if type(lst) == torch.Tensor:
            return lst
        elif type(lst[0]) == torch.Tensor:
            return torch.stack(lst, dim=0)
        else:  # if the elements of lst are floats or something like that
            return torch.tensor(lst)
    current_dimension_i = len(lst)
    for d_i in range(current_dimension_i):
        tensor = tensorify(lst[d_i])
        lst[d_i] = tensor
    # end of loop lst[d_i] = tensor([D_i, ... D_0])
    tensor_lst = torch.stack(lst, dim=0)
    return tensor_lst


def get_device_for_tensor(tensor):
    return torch.device(f"cuda:{tensor.get_device()}")


def to_device(tensors, device):
    device = if_none(device, default_device)
    if is_listy(tensors):
        return [to_device(o, device) for o in tensors]
    return tensors.to(device)


lookup = {
    "num_cpus": num_cpus,
    "default_cpus": default_cpus,
    "default_device": default_device,
    "make_one_hot": make_one_hot,
    "get_device_for_tensor": get_device_for_tensor,
    "to_device": to_device,
    "tensorify": tensorify,
}
