import torch
import torch.utils

from .....vision.tasks.image_segmentation.data.sample import create_segmentation_sample


class SegmentationAugmentationMixin:
    def augment(self, image, mask=None, weight_map=None):
        if self.augment_fn is None:
            return image, mask, weight_map

        if mask is None and weight_map is None:
            return self.augment_fn(image=image)["image"], None, None

        if mask is not None and weight_map is not None:
            augmented = self.augment_fn(image=image, masks=[mask, weight_map])
            return augmented["image"], augmented["masks"][0], augmented["masks"][1]

        if mask is not None:
            augmented = self.augment_fn(image=image, masks=[mask])
            return augmented["image"], augmented["masks"][0], None

        raise NotImplementedError("Nothing has been implemented for a combination of images and weight_maps")


class ImageSegmentationDataset(torch.utils.data.Dataset, SegmentationAugmentationMixin):
    def __init__(
        self,
        samples_data,
        create_sample_fn=lambda sample_data: create_segmentation_sample(**sample_data),
        augment_fn=None,
        tile_fn=None,
        convert_image_to_tensor_fn=lambda image: torch.from_numpy(image.transpose(2, 0, 1)).float(),
        convert_mask_to_tensor_fn=lambda mask: torch.from_numpy(mask.transpose(2, 0, 1)).float(),
    ):
        super().__init__()
        self.samples_data = samples_data
        self.create_sample_fn = create_sample_fn
        self.augment_fn = augment_fn
        self.tile_fn = tile_fn
        self.convert_image_to_tensor_fn = convert_image_to_tensor_fn
        self.convert_mask_to_tensor_fn = convert_mask_to_tensor_fn

    def __len__(self):
        return len(self.samples_data)

    def __getitem__(self, i):
        sample = self.create_sample_fn(self.samples_data[i])
        image, mask, weight_map, _ = sample.data
        image, mask, weight_map = self.augment(image, mask, weight_map)

        sample.image.data = image

        if self.tile_fn is not None:
            image_tiles = self.tile_fn(image)

        if self.convert_image_to_tensor_fn is not None:
            if self.tile_fn is not None:
                sample.image.tensor = torch.stack([self.convert_image_to_tensor_fn(image_tile) for image_tile in image_tiles])
            else:
                sample.image.tensor = self.convert_image_to_tensor_fn(image)

        if sample.has_mask:

            sample.mask.data = mask

            if self.tile_fn is not None:
                mask_tiles = self.tile_fn(mask)

            if self.convert_mask_to_tensor_fn is not None:
                if self.tile_fn is not None:
                    sample.mask.tensor = torch.stack([self.convert_mask_to_tensor_fn(mask_tile) for mask_tile in mask_tiles])
                else:
                    sample.mask.tensor = self.convert_mask_to_tensor_fn(mask)
        return sample


def image_segmentation_collate_fn(samples):
    """Hook to be called before returning the data to the DataLoader

    :param sample: [description]
    :type sample: dict
    """

    batch = {}
    has_tiles = len(samples[0].image.tensor.shape) == 4
    has_mask = samples[0].has_mask

    batch["names"] = {"data": torch.utils.data.dataloader.default_collate([s.name for s in samples])}

    batch["images"] = (
        torch.utils.data.dataloader.default_collate([s.image.tensor for s in samples])
        if not has_tiles
        else torch.vstack([s.image.tensor for s in samples])
    )

    if has_mask:
        batch["masks"] = (
            torch.utils.data.dataloader.default_collate([s.mask.tensor for s in samples])
            if not has_tiles
            else torch.vstack([s.mask.tensor for s in samples])
        )
    return batch


lookup = {"ImageSegmentationDataset": ImageSegmentationDataset, "image_segmentation_collate_fn": image_segmentation_collate_fn}
