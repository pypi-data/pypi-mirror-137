from .cadene import lookup as cadene_model_lookup
from .torchvision import lookup as torchvision_lookup
from .unet import lookup as unet_lookup

models_lookup = {**cadene_model_lookup, **unet_lookup, **torchvision_lookup}
