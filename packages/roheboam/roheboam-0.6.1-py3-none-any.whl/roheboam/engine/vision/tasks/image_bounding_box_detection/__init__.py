from .data import lookup as data_lookup
from .deployment import lookup as deployment_lookup
from .loaders import lookup as loaders_lookup
from .modules import lookup as modules_lookup

lookup = {**data_lookup, **loaders_lookup, **modules_lookup, **deployment_lookup}
