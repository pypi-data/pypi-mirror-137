import importlib

import albumentations
from albumentations import Compose
from albumentations.augmentations.crops.transforms import __all__ as albumentation_crop_transforms
from albumentations.augmentations.geometric.resize import __all__ as albumentation_geometric_resize
from albumentations.augmentations.geometric.rotate import __all__ as albumentation_geometric_rotate
from albumentations.augmentations.geometric.transforms import __all__ as albumentation_geometric_transforms
from albumentations.augmentations.transforms import __all__ as albumentation_transforms

# from albumentations.augmentations.geometric.functional import (
#     __all__ as albumentation_geometric_functional,
# )


def create_augmentation_fn(aug_fns, **kwargs):
    return Compose(aug_fns, p=1, **kwargs)


def import_albumentation_submodule(submodule_functions, submodule_string):
    return {name: getattr(importlib.import_module(submodule_string), name) for name in submodule_functions}


albumentation_lookup = {
    "Compose": albumentations.Compose,
    "BboxParams": albumentations.BboxParams,
    "create_augmentation_fn": create_augmentation_fn,
    **import_albumentation_submodule(albumentation_transforms, "albumentations.augmentations.transforms"),
    **import_albumentation_submodule(albumentation_crop_transforms, "albumentations.augmentations.crops.transforms"),
    # **import_albumentation_submodule(
    #     albumentation_geometric_functional,
    #     "albumentations.augmentations.geometric.functional",
    # ),
    **import_albumentation_submodule(albumentation_geometric_rotate, "albumentations.augmentations.geometric.rotate"),
    **import_albumentation_submodule(albumentation_geometric_resize, "albumentations.augmentations.geometric.resize"),
    **import_albumentation_submodule(albumentation_geometric_transforms, "albumentations.augmentations.geometric.transforms"),
}
