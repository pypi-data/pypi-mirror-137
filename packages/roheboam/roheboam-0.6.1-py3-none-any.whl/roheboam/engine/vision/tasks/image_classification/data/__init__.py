from .dataset import *
from .dataset import lookup as data_lookup
from .sample import *
from .sample import lookup as sample_lookup

lookup = {**data_lookup, **sample_lookup}
