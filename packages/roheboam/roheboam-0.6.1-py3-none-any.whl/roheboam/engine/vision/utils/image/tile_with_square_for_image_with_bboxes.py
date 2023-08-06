import albumentations
import cv2
import numpy as np
from albumentations.augmentations import Crop, PadIfNeeded

from ....utils.convenience import find_nearest_greater_divisible
from ....vision.core.augmentations import create_augmentation_fn


def create_tiled_square_crops_for_image_with_bboxes(image, bboxes, labels, size=256):
    image, bboxes, labels = create_padded_image_with_bboxes(image, bboxes, labels, size)
    tile_coordinates = create_square_tile_coordinates(image, size=size)
    tiled_images_with_bboxes = create_tiles_for_image_with_bboxes(tile_coordinates, image, bboxes, labels)
    return tiled_images_with_bboxes


def create_padded_image_with_bboxes(image, bboxes, labels, size=256):
    height, width, *_ = image.shape
    output = create_augmentation_fn(
        aug_fns=[
            PadIfNeeded(
                find_nearest_greater_divisible(height, size), find_nearest_greater_divisible(width, size), border_mode=cv2.BORDER_CONSTANT, value=0
            )
        ],
        bbox_params=albumentations.BboxParams(format="pascal_voc", label_fields=["labels"]),
    )(image=image, bboxes=bboxes, labels=labels)
    return output["image"], output["bboxes"], output["labels"]


def create_square_tile_coordinates(array, size):
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


def create_tiles_for_image_with_bboxes(tile_coordinates, image, bboxes, labels):
    tiled_image_with_bboxes = []
    for tile_coordinate in tile_coordinates:
        output = create_augmentation_fn(
            aug_fns=[Crop(**tile_coordinate)], bbox_params=albumentations.BboxParams(format="pascal_voc", label_fields=["labels"])
        )(image=image, bboxes=bboxes, labels=labels)
        tiled_image_with_bboxes.append((output["image"], output["bboxes"], output["labels"]))
    return tiled_image_with_bboxes
