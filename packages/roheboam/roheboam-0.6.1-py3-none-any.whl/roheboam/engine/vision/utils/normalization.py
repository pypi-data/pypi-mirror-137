from functools import partial

import numpy as np
import torch

from ...utils.training import get_device_for_tensor, to_device


def normalize_image(image, *, mean, std):
    assert image.dtype == np.float32
    denominator = np.reciprocal(std, dtype=np.float32)
    image -= mean
    image *= denominator
    return image


def unnormalize_image(image, *, mean, std):
    assert image.dtype == np.float32
    denominator = np.reciprocal(std, dtype=np.float32)
    image /= denominator
    image += mean
    return image


def normalize_tensor(tensor, *, mean, std):
    mean = torch.Tensor(mean)
    std = torch.Tensor(std)

    if tensor.is_cuda:
        device = get_device_for_tensor(tensor)
        mean = to_device(mean, device)
        std = to_device(std, device)

    tensor = (tensor - mean[..., None, None]) / std[..., None, None]
    return tensor


def unnormalize_tensor(tensor, *, mean, std):
    mean = torch.Tensor(mean)
    std = torch.Tensor(std)

    if tensor.is_cuda:
        device = get_device_for_tensor(tensor)
        mean = to_device(mean, device)
        std = to_device(std, device)

    tensor = tensor * std[..., None, None] + mean[..., None, None]
    return tensor


IMAGE_NET_STATS = {"mean": [0.485, 0.456, 0.406], "std": [0.229, 0.224, 0.225]}

FOUR_CHANNEL_PNASNET5LARGE_STATS = {"mean": [0.5, 0.5, 0.5, 0.5], "std": [0.5, 0.5, 0.5, 0.5]}

FOUR_CHANNEL_IMAGE_NET_STATS = {"mean": [0.485, 0.456, 0.406, 0.485], "std": [0.229, 0.224, 0.224, 0.229]}
image_net_normalize = partial(normalize_tensor, **IMAGE_NET_STATS)
image_net_denormalize = partial(unnormalize_tensor, **IMAGE_NET_STATS)

four_channel_image_net_normalize = partial(normalize_tensor, **FOUR_CHANNEL_IMAGE_NET_STATS)
four_channel_image_net_denormalize = partial(unnormalize_tensor, **FOUR_CHANNEL_IMAGE_NET_STATS)

four_channel_pnasnet5large_normalize = partial(normalize_tensor, **FOUR_CHANNEL_PNASNET5LARGE_STATS)
four_channel_pnasnet5large_denormalize = partial(unnormalize_tensor, **FOUR_CHANNEL_PNASNET5LARGE_STATS)

lookup = {
    "normalize_tensor": normalize_tensor,
    "unnormalize_tensor": unnormalize_tensor,
    "normalize_image": normalize_image,
    "unnormalize_image": unnormalize_image,
    "image_net_denormalize": image_net_denormalize,
    "four_channel_image_net_unnormalize": four_channel_image_net_denormalize,
    "four_channel_pnasnet5large_unnormalize": four_channel_image_net_denormalize,
    "image_net_normalize": image_net_normalize,
    "four_channel_image_net_normalize": four_channel_image_net_normalize,
    "four_channel_pnasnet5large_normalize": four_channel_image_net_normalize,
    "identity": lambda x: x,
}
