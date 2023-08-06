import numpy as np
import torch
import torch.utils


class ImageBoundingBoxDetectionAugmentationMixin:
    def augment(self, image, bboxes, labels):
        if self.augment_fn is None:
            return image, bboxes, labels

        result = self.augment_fn(image=image, bboxes=bboxes, class_labels=labels)
        image = result["image"]
        bboxes = np.array(result["bboxes"])
        labels = np.array(result["class_labels"])
        return image, bboxes, labels


# class ImageBoundingBoxDetectionDataset(torch.utils.data.Dataset, ImageBoundingBoxDetectionAugmentationMixin):
#     def __init__(
#         self,
#         samples_data,
#         create_sample_fn=lambda sample_data: sample_data,
#         augment_fn=None,
#         tile_fn=None,
#         convert_image_to_tensor_fn=None,
#         convert_bboxes_to_tensor_fn=None,
#     ):
#         self.samples_data = samples_data
#         self.create_sample_fn = create_sample_fn
#         self.augment_fn = augment_fn
#         self.tile_fn = tile_fn
#         self.convert_image_to_tensor_fn = convert_image_to_tensor_fn
#         self.convert_bboxes_to_tensor_fn = convert_bboxes_to_tensor_fn

#     def __len__(self):
#         return len(self.samples_data)

#     def __getitem__(self, i):
#         sample = self.create_sample_fn(self.samples_data[i])
#         image, bboxes, labels, _ = sample.data
#         image, bboxes, labels = self.augment(image, bboxes, labels)

#         sample.image.data = image

#         if self.tile_fn is not None:
#             image_tiles = self.tile_fn(image)

#         if self.convert_image_to_tensor_fn is not None:
#             if self.tile_fn is not None:
#                 sample.image.tensor = torch.stack([self.convert_image_to_tensor_fn(image_tile) for image_tile in image_tiles])
#             else:
#                 sample.image.tensor = self.convert_image_to_tensor_fn(image)

#         if sample.labels_exists:

#             sample.bboxes.data = bboxes

#             if self.tile_fn is not None:
#                 bboxes_tiles = self.tile_fn(bboxes)

#             if self.convert_bboxes_to_tensor_fn is not None:
#                 if self.tile_fn is not None:
#                     sample.bboxes.tensor = torch.stack([self.convert_bboxes_to_tensor_fn(bbox_tile) for bbox_tile in bboxes_tiles])
#                 else:
#                     sample.bboxes.tensor = self.convert_bboxes_to_tensor_fn(bboxes)
#             sample.labels.tensor = torch.from_numpy(labels)
#         return sample


class ImageBoundingBoxDetectionDatasetV2(torch.utils.data.Dataset, ImageBoundingBoxDetectionAugmentationMixin):
    def __init__(
        self,
        samples,
        augment_fn=None,
        tile_fn=None,
        convert_image_to_tensor_fn=lambda image: torch.from_numpy(image),
        convert_bboxes_to_tensor_fn=lambda bboxes: torch.from_numpy(bboxes),
    ):
        self.samples = samples
        self.augment_fn = augment_fn
        self.tile_fn = tile_fn
        self.convert_image_to_tensor_fn = convert_image_to_tensor_fn
        self.convert_bboxes_to_tensor_fn = convert_bboxes_to_tensor_fn

    def __len__(self):
        return len(self.samples)

    def __getitem__(self, i):
        sample = self.samples[i]
        data = {}
        data["name"] = sample.name
        image, bboxes, labels, _ = sample.data
        image, bboxes, labels = self.augment(image, bboxes, labels)

        if self.tile_fn is not None:
            image_tiles = self.tile_fn(image)

        if self.convert_image_to_tensor_fn is not None:
            if self.tile_fn is not None:
                data["image"] = torch.stack([self.convert_image_to_tensor_fn(image_tile) for image_tile in image_tiles])
            else:
                data["image"] = self.convert_image_to_tensor_fn(image)

        if sample.labels_exists:
            if self.tile_fn is not None:
                bboxes_tiles = self.tile_fn(bboxes)

            if self.convert_bboxes_to_tensor_fn is not None:
                if self.tile_fn is not None:
                    data["boxes"] = torch.stack([self.convert_bboxes_to_tensor_fn(bbox_tile) for bbox_tile in bboxes_tiles])
                else:
                    data["boxes"] = self.convert_bboxes_to_tensor_fn(bboxes)
            data["labels"] = torch.from_numpy(labels)
        return data


def image_bounding_box_detection_torchvision_collate_fn(samples):
    # batch = {}
    # names = [s.name for s in samples]
    # batch["names"] = names
    # batch["images"] = [s.image.tensor.float() for s in samples]

    # has_bbox_and_labels = samples[0].labels_exists and samples[0].bboxes_exists
    # if has_bbox_and_labels:
    #     batch["targets"] = []
    #     for s in samples:
    #         boxes = s.bboxes.tensor.float()
    #         labels = s.labels.tensor.type(torch.int64)
    #         if len(boxes) == 0:
    #             boxes = torch.zeros((0, 4), dtype=torch.float32)
    #             labels = torch.zeros((1, 1), dtype=torch.int64)
    #         batch["targets"].append({"boxes": boxes, "labels": labels})
    batch = {}
    batch["names"] = [s["name"] for s in samples]
    batch["images"] = [s["image"].float() for s in samples]

    has_bbox_and_labels = "labels" in samples[0] and "boxes" in samples[0]
    if has_bbox_and_labels:
        batch["targets"] = []
        for sample in samples:
            boxes = sample["boxes"].float()
            labels = sample["labels"].type(torch.int64)
            if len(boxes) == 0:
                boxes = torch.zeros((0, 4), dtype=torch.float32)
                labels = torch.zeros((1, 1), dtype=torch.int64)
            batch["targets"].append({"boxes": boxes, "labels": labels})
    return batch


lookup = {
    # "ImageBoundingBoxDetectionDataset": ImageBoundingBoxDetectionDataset,
    "ImageBoundingBoxDetectionDatasetV2": ImageBoundingBoxDetectionDatasetV2,
    "image_bounding_box_detection_torchvision_collate_fn": image_bounding_box_detection_torchvision_collate_fn,
}
