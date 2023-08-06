import cv2
import numpy as np
from albumentations.augmentations import Crop, PadIfNeeded

from ....utils.convenience import find_nearest_greater_divisible


def create_tiled_square_crops(array, size=256):
    padded_array = create_padded_array(array, size)
    crop_areas = create_square_crop_areas(padded_array, size=size)
    cropped_arrays = create_crops(crop_areas, padded_array)
    return cropped_arrays


def merge_tiled_square_crops(tiles, original_height, original_width, size=256):
    padded_height = find_nearest_greater_divisible(original_height, size)
    padded_width = find_nearest_greater_divisible(original_width, size)
    n_tiles_in_height = padded_height // size
    n_tiles_in_width = padded_width // size
    n_tiles_per_image = n_tiles_in_height * n_tiles_in_width
    merged_images = []
    for i in range(0, len(tiles), n_tiles_per_image):
        merged_images.append(merge_tiled_square_crops_for_single(tiles[i : i + n_tiles_per_image], padded_height, padded_width, size))
    return merged_images


def merge_tiled_square_crops_for_single(tiles_for_image, original_height, original_width, size=256):
    merged_horizontal_tiles = []
    n_tiles_in_height = original_height // size
    n_tiles_in_width = original_width // size
    for i in range(0, len(tiles_for_image), n_tiles_in_width):
        merged_horizontal_tiles.append(np.hstack(tiles_for_image[i : i + n_tiles_in_width]))
    assert len(merged_horizontal_tiles) == n_tiles_in_height
    return np.vstack(merged_horizontal_tiles)


def create_padded_array(array, size=256):
    height, width, *_ = array.shape
    padded = PadIfNeeded(
        find_nearest_greater_divisible(height, size), find_nearest_greater_divisible(width, size), border_mode=cv2.BORDER_CONSTANT, value=0
    )(image=array)["image"]
    return padded


def create_crops(crop_areas, array):
    cropped_arrays = []
    for crop_area in crop_areas:
        cropped = Crop(**crop_area)(image=array)
        cropped_arrays.append(cropped["image"])
    return cropped_arrays


def create_square_crop_areas(array, size):
    crops = []
    height, width, *_ = array.shape
    for i in range(height // size):
        for j in range(width // size):
            x_min = j * size
            y_min = i * size
            x_max = (j + 1) * size
            y_max = (i + 1) * size
            crops.append({"x_min": x_min, "y_min": y_min, "x_max": x_max, "y_max": y_max})
            assert x_max - x_min == size
            assert y_max - y_min == size
    return crops


lookup = {
    "create_tiled_square_crops": create_tiled_square_crops,
    "merge_tiled_square_crops": merge_tiled_square_crops,
    "create_square_crop_areas": create_square_crop_areas,
    "create_crops": create_crops,
    "create_padded_array": create_padded_array,
    "merge_tiled_square_crops_for_single": merge_tiled_square_crops_for_single,
}
