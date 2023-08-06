from .loading import lookup as loading_lookup
from .saving import lookup as saving_lookup

lookup = {**saving_lookup, **loading_lookup}
