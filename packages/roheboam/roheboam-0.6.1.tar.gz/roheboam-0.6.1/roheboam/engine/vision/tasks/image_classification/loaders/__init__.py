try:
    from .activeloop import *
    from .activeloop import lookup as activeloop_lookup
    from .label_per_folder import *
    from .label_per_folder import lookup as label_per_folder_lookup

    lookup = {**label_per_folder_lookup, **activeloop_lookup}
except Exception:
    from .label_per_folder import *
    from .label_per_folder import lookup as label_per_folder_lookup

    lookup = {**label_per_folder_lookup}
