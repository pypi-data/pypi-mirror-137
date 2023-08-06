from .callback import *
from .callback import lookup as callback_lookup
from .module import *
from .module import lookup as module_lookup

lookup = {**callback_lookup, **module_lookup}
