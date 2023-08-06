from .dataset import *
from .dataset import lookup as dataset_lookup
from .sample import *
from .sample import lookup as sample_lookup

lookup = {**dataset_lookup, **sample_lookup}
