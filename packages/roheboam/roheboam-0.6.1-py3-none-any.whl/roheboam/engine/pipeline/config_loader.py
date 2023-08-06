from copy import deepcopy
from functools import reduce
from pathlib import Path

import yaml

from ..logger import logger
from .constants import RESOURCE_KEY, VARIABLE_KEY
from .yaml_loader import RoheboamYamlDumper, RoheboamYamlLoader, Variable


def load_config_from_strings(config_strings, with_variable_replacement=False):
    configs = [load_config_from_string(s, with_variable_replacement=False) for s in config_strings]
    merged_configs = merge_dicts(configs)

    if with_variable_replacement:
        merged_configs = replace_config_variables(merged_configs, resource_key=RESOURCE_KEY, variable_key=VARIABLE_KEY)

    return merged_configs


def load_config_from_string(config_string, with_variable_replacement=False):
    config = yaml.load(config_string, Loader=RoheboamYamlLoader)
    if with_variable_replacement:
        config = replace_config_variables(config, resource_key=RESOURCE_KEY, variable_key=VARIABLE_KEY)
    return config


def load_config_from_path(path, with_variable_replacement=False):
    with Path(path).open("r") as f:
        config = load_config_from_string(f, with_variable_replacement)
    return config


def load_config_from_paths(paths, with_variable_replacement=False):

    configs = [load_config_from_path(p, with_variable_replacement=False) for p in paths]
    merged_configs = merge_dicts(configs)

    if with_variable_replacement:
        merged_configs = replace_config_variables(merged_configs, resource_key=RESOURCE_KEY, variable_key=VARIABLE_KEY)
    return merged_configs


def dump_config_to_string(config):
    return yaml.dump(config, Dumper=RoheboamYamlDumper, default_flow_style=False)


def dump_config_to_path(config, save_path):
    path = Path(save_path)
    path.parent.mkdir(exist_ok=True, parents=True)
    with path.open("w") as yaml_file:
        yaml.dump(config, yaml_file, Dumper=RoheboamYamlDumper, default_flow_style=False)


def replace_config_variables(config, resource_key=RESOURCE_KEY, variable_key=VARIABLE_KEY):
    if variable_key not in config:
        logger.warning("No variables passed to pipeline")
        return config

    config = deepcopy(config)
    replaced_resources = replace_variables(config[resource_key], config[variable_key])
    config[resource_key] = replaced_resources
    return config


def replace_variables(resources, variables):
    if isinstance(resources, dict):
        for name, resource in resources.items():
            resources[name] = replace_variables(resource, variables)
    elif isinstance(resources, list):
        for i, resource in enumerate(resources):
            resources[i] = replace_variables(resource, variables)
    elif isinstance(resources, Variable):
        try:
            if resources.is_nested:
                resources = replace_variable_with_group(resources, variables)
            else:
                resources = replace_variable_without_group(resources, variables)
        except Exception as e:
            logger.error(f"See if there are any nodes using variable: {resources.variable_group}.{resources.variable_name}")
            raise e

    else:
        return resources
    return resources


def replace_variable_with_group(resource, variables):
    for i, subgroup_name in enumerate(resource.variable_groups):
        if i == 0:
            variable = variables[subgroup_name]
        else:
            variable = variable[subgroup_name]
    return variable[resource.variable_name]


def replace_variable_without_group(resources, variables):
    return variables[resources.variable_name]


def merge_dicts(dicts):
    def merge(d1, d2):
        def _merge(d1, d2, path=None):
            # Keep function pure by creating new instance
            #     d1 = dict(d1)
            if path is None:
                path = []
            for key in d2:
                if key in d1:
                    if isinstance(d1[key], dict) and isinstance(d2[key], dict):
                        _merge(d1[key], d2[key], path + [str(key)])
                    elif d1[key] == d2[key]:
                        pass  # same leaf value
                    else:
                        raise Exception("Conflict at %s" % ".".join(path + [str(key)]))
                else:
                    d1[key] = d2[key]
            return d1

        return _merge(dict(d1), d2)

    return reduce(merge, dicts)
