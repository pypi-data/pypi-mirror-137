try:
    from .activeloop import *
    from .activeloop import lookup as activeloop_lookup
    from .from_paths import *
    from .from_paths import lookup as from_paths_lookup

    lookup = {**activeloop_lookup, **from_paths_lookup}
except Exception:
    from .from_paths import *
    from .from_paths import lookup as from_paths_lookup

    lookup = {**from_paths_lookup}
