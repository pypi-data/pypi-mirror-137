import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torchvision

from .....utils.model import model_sizes
from ..utils.layers import conv2d, conv2d_relu, conv2d_trans


class UnetBlock(nn.Module):
    "A basic U-Net block."

    def __init__(self, up_in_c, x_in_c, hook):
        super().__init__()
        self.hook = hook
        ni = up_in_c
        self.upconv = conv2d_trans(ni, ni // 2)  # H, W -> 2H, 2W
        ni = ni // 2 + x_in_c
        self.conv1 = conv2d(ni, ni // 2)
        ni = ni // 2
        self.conv2 = conv2d(ni, ni)
        self.bn = nn.BatchNorm2d(ni)

    def forward(self, up_in):
        up_out = self.upconv(up_in)

        try:
            cat_x = torch.cat([up_out, self.hook.stored], dim=1)
        except Exception as e:
            import pdb

            pdb.set_trace()
            print(e)
            pass
        x = F.relu(self.conv1(cat_x))
        x = F.relu(self.conv2(x))
        return self.bn(x)


class DynamicUnet(nn.Sequential):
    "Create a U-Net from a given architecture."

    def __init__(self, encoder, n_classes):
        imsize = (256, 256)
        sfs_szs, x, self.sfs = model_sizes(encoder, size=imsize)
        sfs_idxs = reversed(_get_sfs_idxs(sfs_szs))

        ni = sfs_szs[-1][1]
        middle_conv = nn.Sequential(conv2d_relu(ni, ni * 2, bn=True), conv2d_relu(ni * 2, ni, bn=True))
        x = middle_conv(x)
        layers = [encoder, nn.ReLU(), middle_conv]

        for idx in sfs_idxs:
            up_in_c, x_in_c = int(x.shape[1]), int(sfs_szs[idx][1])
            unet_block = UnetBlock(up_in_c, x_in_c, self.sfs[idx])
            layers.append(unet_block)
            x = unet_block(x)

        ni = unet_block.conv2.out_channels
        if imsize != sfs_szs[0][-2:]:
            layers.append(conv2d_trans(ni, ni))
        layers.append(conv2d(ni, n_classes, 1))
        super().__init__(*layers)

    def __del__(self):
        if hasattr(self, "sfs"):
            self.sfs.remove()


def _get_sfs_idxs(sizes):
    "Get the indexes of the layers where the size of the activation changes."
    feature_szs = [size[-1] for size in sizes]
    sfs_idxs = list(np.where(np.array(feature_szs[:-1]) != np.array(feature_szs[1:]))[0])
    if feature_szs[0] != feature_szs[1]:
        sfs_idxs = [0] + sfs_idxs
    return sfs_idxs


def create_encoder(name, pretrained=True):
    if name == "pytorch_resnet18":
        return nn.Sequential(*list(torchvision.models.resnet.resnet18(pretrained=pretrained).children())[:-2])
    elif name == "pytorch_resnet34":
        return nn.Sequential(*list(torchvision.models.resnet.resnet34(pretrained=pretrained).children())[:-2])
    elif name == "pytorch_resnet50":
        return nn.Sequential(*list(torchvision.models.resnet.resnet50(pretrained=pretrained).children())[:-2])
    elif name == "pytorch_resnet101":
        return nn.Sequential(*list(torchvision.models.resnet.resnet101(pretrained=pretrained).children())[:-2])
    elif name == "pytorch_resnet152":
        return nn.Sequential(*list(torchvision.models.resnet.resnet152(pretrained=pretrained).children())[:-2])
    else:
        print(f"A method to extract the encoder from {name} is not defined")


def unet_with_resnet18_backbone(n_classes=1, pretrained=True, include_encoder=False):
    encoder = create_encoder("pytorch_resnet18", pretrained=pretrained)
    unet = DynamicUnet(encoder, n_classes=n_classes)
    if include_encoder:
        return encoder, unet
    return unet


def unet_with_resnet34_backbone(n_classes=1, pretrained=True, include_encoder=False):
    encoder = create_encoder("pytorch_resnet34", pretrained=pretrained)
    unet = DynamicUnet(encoder, n_classes=n_classes)
    if include_encoder:
        return encoder, unet
    return unet


def unet_with_resnet50_backbone(n_classes=1, pretrained=True, include_encoder=False):
    encoder = create_encoder("pytorch_resnet50", pretrained=pretrained)
    unet = DynamicUnet(encoder, n_classes=n_classes)
    if include_encoder:
        return encoder, unet
    return unet


def unet_with_resnet101_backbone(n_classes=1, pretrained=True, include_encoder=False):
    encoder = create_encoder("pytorch_resnet101", pretrained=pretrained)
    unet = DynamicUnet(encoder, n_classes=n_classes)
    if include_encoder:
        return encoder, unet
    return unet


def unet_with_resnet152_backbone(n_classes=1, pretrained=True, include_encoder=False):
    encoder = create_encoder("pytorch_resnet152", pretrained=pretrained)
    unet = DynamicUnet(encoder, n_classes=n_classes)
    if include_encoder:
        return encoder, unet
    return unet
