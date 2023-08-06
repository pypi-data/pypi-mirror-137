try:
    # TODO: remove if not supporting activeloop
    from .activeloop import *
    from .activeloop import lookup as activeloop_lookup
    from .roheboam import *
    from .roheboam import lookup as roheboam_lookup
    from .ultralytics import *
    from .ultralytics import lookup as ultralytics_lookup

    lookup = {**ultralytics_lookup, **activeloop_lookup, **roheboam_lookup}
except Exception:
    from .roheboam import *
    from .roheboam import lookup as roheboam_lookup
    from .ultralytics import *
    from .ultralytics import lookup as ultralytics_lookup

    lookup = {**ultralytics_lookup, **roheboam_lookup}
