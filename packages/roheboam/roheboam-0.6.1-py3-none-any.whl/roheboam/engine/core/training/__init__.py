from .data import lookup as data_lookup
from .splitting import lookup as splitting_lookup

lookup = {**data_lookup, **splitting_lookup}
