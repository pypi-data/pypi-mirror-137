from functools import partial

import cv2
import numpy as np

try:
    import pyvips
except Exception:
    pass
import torch

from ....utils.training import make_one_hot
from .io import *
from .io import lookup as io_lookup
from .plot import *
from .plot import lookup as plot_lookup
from .tile_with_square import *
from .tile_with_square import lookup as tile_with_square_lookup


def image_to_tensor(image, normalize_image_fn=None, scale_to_range_fn=None, normalize_tensor_fn=None):
    """Transforms an image to a tensor

    :param image: image
    :type image: numpy.array
    :param normalize_image_fn: function to normalize image, look at: pytorch_toolbox.vision.utils.normalization.normalize_image, defaults to None
    :type normalize_image_fn: Callable, optional
    :param scale_to_range_fn: function to transform an image to a certain range, look at: pytorch_toolbox.vision.utils._utils.scale_to_range,
    defaults to None
    :type scale_to_range_fn: Callable, optional
    :param normalize_tensor_fn: function to normalize the tensor, look at: pytorch_toolbox.vision.utils.normalization.normalize, defaults to None
    :type normalize_tensor_fn: Callable, optional
    :return: Tensor
    :rtype: torch.Tensor
    """

    n_dims = len(image.shape)
    assert len(image.shape) in [2, 3], "There must be two, or three dimensions to the image"
    if n_dims == 2:
        image = np.expand_dims(image, -1)

    if image.dtype != np.float32:
        image = image.astype(np.float32)

    if normalize_image_fn is not None:
        image = normalize_image_fn(image)

    if scale_to_range_fn is not None:
        image = scale_to_range_fn(image)

    tensor = numpy_image_to_tensor(image)

    if normalize_tensor_fn is not None:
        tensor = normalize_tensor_fn(tensor)

    return tensor


def tensor_to_image(tensor, unnormalize_image_fn=None, unscale_to_range_fn=None, unnormalize_tensor_fn=None, convert_to_image_type_fn=None):
    assert len(tensor.shape) in [3, 4], "There must be three dimensions in the tensor C x H x W or B x C x H x W"
    if unnormalize_tensor_fn is not None:
        tensor = unnormalize_tensor_fn(tensor)

    image = tensor_to_numpy_image(tensor)

    if image.dtype != np.float32:
        image = image.astype(np.float32)

    if unscale_to_range_fn is not None:
        image = unscale_to_range_fn(image)

    if unnormalize_image_fn is not None:
        image = unnormalize_image_fn(image)

    if convert_to_image_type_fn is not None:
        image = convert_to_image_type_fn(image)

    return image


def unit_normalized_tensor_to_8_bit_image(tensor):
    return tensor_to_image(
        tensor, unscale_to_range_fn=partial(scale_to_range, original_max_val=1, max_val=255), convert_to_image_type_fn=to_uint8_image
    )


def numpy_image_to_tensor(image):
    if len(image.shape) == 3:
        image = np.transpose(image, (2, 0, 1))
    elif len(image.shape) == 4:
        image = np.transpose(image, (2, 3, 1))
    tensor = torch.from_numpy(image)
    return tensor


def tensor_to_numpy_image(tensor):
    image = tensor.cpu().detach().numpy()
    if len(tensor.shape) == 3:
        image = np.transpose(image, (1, 2, 0))
    elif len(tensor.shape) == 4:
        image = np.transpose(image, (0, 2, 3, 1))

    return image


def is_rgb(image):
    return len(image.shape) == 3 and image.shape[-1] == 3


def to_rgb(image):
    if is_rgb(image):
        return image
    else:
        # Catch case where we have (H x W x 1)
        image = image.squeeze()
    return np.stack([image] * 3, axis=-1)


def to_uint8_image(image, clip=True):
    image = np.array(image)
    if clip:
        image = np.clip(image, a_min=0, a_max=255)
    return image.astype(np.uint8)


def scale_to_range(image, original_min_val=0, min_val=0, original_max_val=255, max_val=1):
    scaled_image = (max_val - min_val) * (image - min_val) / (original_max_val - original_min_val) + min_val
    return scaled_image


def create_mask_from_vertices(vertices, image_width=None, image_height=None):
    """Create mask from a list of vertices

    :param vertices: list of vertices in OpenCV format
    :type vertices: [[x1, y2], [x2, y2], ...]
    :param image_width: [description], defaults to None
    :type image_width: [type], optional
    :param image_height: [description], defaults to None
    :type image_height: [type], optional
    :return: [description]
    :rtype: [type]
    """
    xs = [p[0] for p in vertices]
    ys = [p[1] for p in vertices]

    if image_width is None:
        image_width = max(xs) + 1

    if image_height is None:
        image_height = max(ys) + 1

    vertices = np.array([vertices], dtype=np.int32)
    img = np.zeros([image_height, image_width], dtype=np.uint8)
    cv2.fillPoly(img, vertices, 1)

    return img


def calculate_pixels_in_mask(mask, value=None):
    if value is None:
        return len(mask[mask > 0])
    else:
        return len(mask[mask == value])


def load_mask_from_grayscale_and_transform_to_one_hot(n_classes):
    return lambda mask_path: make_one_hot(imread_grayscale(mask_path), n_classes=n_classes)


def mask_to_tensor(mask, make_one_hot_fn=None):
    if make_one_hot_fn is not None:
        mask = mask.squeeze()
        mask = make_one_hot_fn(mask)

    tensor = numpy_image_to_tensor(mask)
    return tensor


def tensor_to_mask(tensor, reduce_one_hot_fn=None, convert_to_image_type_fn=None):
    image = tensor_to_numpy_image(tensor)
    if reduce_one_hot_fn is not None:
        image = reduce_one_hot_fn(image)
    if convert_to_image_type_fn is not None:
        image = convert_to_image_type_fn(image)
    return image


def reduce_max_with_dim(array, dim):
    return np.argmax(array, axis=dim)


def set_only_class(mask, only_class=None, binary_mask=True):
    if only_class is None:
        return mask
    mask[mask != only_class] = 0
    if binary_mask:
        mask[mask == only_class] = 1
    return mask


lookup = {
    "calculate_pixels_in_mask": calculate_pixels_in_mask,
    "create_mask_from_vertices": create_mask_from_vertices,
    "image_to_tensor": image_to_tensor,
    "is_rgb": is_rgb,
    "load_mask_from_grayscale_and_transform_to_one_hot": load_mask_from_grayscale_and_transform_to_one_hot,
    "mask_to_tensor": mask_to_tensor,
    "tensor_to_mask": tensor_to_mask,
    "reduce_max_with_dim": reduce_max_with_dim,
    "numpy_image_to_tensor": numpy_image_to_tensor,
    "tensor_to_image": tensor_to_image,
    "tensor_to_numpy_image": tensor_to_numpy_image,
    "to_rgb": to_rgb,
    "to_uint8_image": to_uint8_image,
    "scale_to_range": scale_to_range,
    "unit_normalized_tensor_to_8_bit_image": unit_normalized_tensor_to_8_bit_image,
    "set_only_class": set_only_class,
    **io_lookup,
    **plot_lookup,
    **tile_with_square_lookup,
}
