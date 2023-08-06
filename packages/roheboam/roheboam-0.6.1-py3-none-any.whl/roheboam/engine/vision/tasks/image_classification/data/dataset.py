import torch
import torch.utils.data


class ClassificationAugmentationMixin:
    def augment(self, image):
        if self.augment_fn is not None:
            # image = self.augment_fn(image=image)
            # # TODO: curry albumentations function so we don't have to do this
            # try:
            #     image = image["image"]
            # except KeyError:
            #     pass
            image = self.augment_fn(image=image)["image"]

        return image


class ClassificationTTAMixin:
    def tta(self, image, label=None):
        if self.tta_fn is not None:
            image, label = self.tta_fn(image, label)
        else:
            pass
        return image, label


class ImageClassificationDataset(torch.utils.data.Dataset, ClassificationAugmentationMixin, ClassificationTTAMixin):
    def __init__(self, samples_data, create_sample_fn=lambda x: x, augment_fn=lambda x: x, convert_image_to_tensor_fn=lambda x: x):
        self.samples_data = samples_data
        self.create_sample_fn = create_sample_fn
        self.augment_fn = augment_fn
        self.convert_image_to_tensor_fn = convert_image_to_tensor_fn

    def __len__(self):
        return len(self.samples_data)

    def __getitem__(self, i):
        sample = self.create_sample_fn(self.samples_data[i])
        image, label = sample.data

        image = self.augment(image)
        tensor = self.convert_image_to_tensor_fn(image)

        if sample.has_label:
            sample.label.tensor = label
        sample.image.tensor = tensor
        return sample


def image_classification_collate_fn(samples):
    batch = {}

    batch["names"] = torch.utils.data.dataloader.default_collate([s.name for s in samples])

    batch["images"] = torch.stack([s.image.tensor.type(torch.FloatTensor) for s in samples])

    labels_exists = samples[0].has_label

    if labels_exists:
        batch["labels"] = torch.utils.data.dataloader.default_collate([s.label.tensor for s in samples])
    return batch


lookup = {"ImageClassificationDataset": ImageClassificationDataset, "image_classification_collate_fn": image_classification_collate_fn}
