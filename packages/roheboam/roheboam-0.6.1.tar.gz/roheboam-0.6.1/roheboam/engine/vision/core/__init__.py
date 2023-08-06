from .augmentations import *
from .augmentations import augmentation_lookup
from .models import *
from .models import models_lookup

lookup = {**augmentation_lookup, **models_lookup}
