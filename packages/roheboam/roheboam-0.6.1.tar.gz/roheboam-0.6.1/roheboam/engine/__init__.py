def get_toolbox_lookup():
    from .core import lookup as core_lookup
    from .integrations import lookup as integrations_lookup
    from .pipeline import Pipeline
    from .pipeline.config_loader import load_config_from_path, load_config_from_paths, replace_config_variables
    from .pipeline.utils.lookup_functions import lookup as pipeline_lookup_functions
    from .utils import lookup as utils_lookup
    from .vision import lookup as vision_lookup

    lookup = {
        **core_lookup,
        **integrations_lookup,
        **vision_lookup,
        **pipeline_lookup_functions,
        **utils_lookup,
        "Pipeline": Pipeline,
        "load_config_from_path": load_config_from_path,
        "load_config_from_paths": load_config_from_paths,
        "replace_config_variables": replace_config_variables,
    }
    return lookup
