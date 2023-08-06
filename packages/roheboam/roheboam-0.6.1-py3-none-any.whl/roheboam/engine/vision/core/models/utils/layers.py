import torch.nn as nn


def conv2d_relu(ni, nf, ks=3, stride=1, padding=None, bn=False, bias=False):
    """Create a `conv2d` layer with `nn.ReLU` activation and optional(`bn`) `nn.BatchNorm2d`: `ni` input, `nf` out
    filters, `ks` kernel, `stride`:stride, `padding`:padding, `bn`: batch normalization."""
    layers = [conv2d(ni, nf, ks=ks, stride=stride, padding=padding, bias=bias), nn.ReLU()]
    if bn:
        layers.append(nn.BatchNorm2d(nf))
    return nn.Sequential(*layers)


def conv2d_trans(ni, nf, ks=2, stride=2, padding=0):
    "Create `nn.ConvTranspose2d` layer: `ni` inputs, `nf` outputs, `ks` kernel size, `stride`: stride. `padding` defaults to 0."
    return nn.ConvTranspose2d(ni, nf, kernel_size=ks, stride=stride, padding=padding)


def conv2d(ni, nf, ks=3, stride=1, padding=None, bias=False):
    "Create `nn.Conv2d` layer: `ni` inputs, `nf` outputs, `ks` kernel size. `padding` defaults to `k//2`."
    if padding is None:
        padding = ks // 2
    return nn.Conv2d(ni, nf, kernel_size=ks, stride=stride, padding=padding, bias=bias)
