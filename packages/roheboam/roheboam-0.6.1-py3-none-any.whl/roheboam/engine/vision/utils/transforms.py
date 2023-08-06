from albumentations import Compose


def create_augmentation_fn(aug_fns, **kwargs):
    return Compose(aug_fns, p=1, **kwargs)


lookup = {"create_augmentation_fn": create_augmentation_fn}
