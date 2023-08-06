import importlib.util
import inspect
import pprint
from pathlib import Path

from ...logger import logger


def create_lookup(path, package_name, ignore_paths=[]):
    """Start at `path` and traverses the directory tree and creates a key, value pair lookup for all the
    classes and functions found in *.py files, except for files in ignore_paths

    :param path: root path to start the traversal
    :type path: str or Path
    :param package_name: name of the package for the lookup to be generated, this is needed to generate lookups for relative importss
    :type package_name: str
    :param ignore_paths: paths to ignore for lookup creation, defaults to []
    :type ignore_paths: list, optional
    :return: a lookup dictionary that can be used by the Pipeline
    :rtype: dict
    """
    lookup = {}
    for p in Path(path).glob("*"):
        if p in ignore_paths:
            lookup = {**lookup}
            logger.info(f"Ignoring file: {str(p)}")
        elif p.suffix == ".py":
            logger.info(f"Found file: {str(p)} and creating lookup")
            created_lookup = create_lookup_from_path(p, package_name)
            logger.info(f"Created lookup: {pprint.pformat(created_lookup)}")
            lookup = {**lookup, **created_lookup}
        elif p.is_dir():
            logger.info(f"Found folder: {str(p)}")
            lookup = {**lookup, **create_lookup(p, package_name, ignore_paths)}
        else:
            logger.info(f"Nothing here: {str(p)}")
            lookup = {**lookup}
    # logger.info(f"Current lookup is: {pprint.pformat(lookup)}")

    return lookup


def create_lookup_from_path(path, package_name):
    try:
        # logger.info(f"Creating lookup from path: {str(path)}")
        module = load_module_from_path(path, package_name)
        lookup = create_lookup_from_module(module)
        # logger.info(f"Lookup generated: {lookup}")
        return lookup
    except ImportError as e:
        if str(e) == "attempted relative import with no known parent package":
            logger.info(f"Importing of module from path: {path} has failed")
            logger.info(e)
            return {}
        else:
            logger.error(f"Importing of module from path: {path} has failed")
            logger.error(e)
            raise ImportError


def load_module_from_path(path, package_name):
    """Create a module the path

    For example:

    path = Path(/home/kevin/Documents/Projects/pytorch-toolbox/pytorch_toolbox/pipeline/utils/saving.py)
    module_name = saving
    full_module_name = pytorch_toolbox.pipeline.utils.saving

    :param path: Full path to a module
    :type path: Path
    :param package_name: name of the package for the lookup to be generated
    :type package_name: str

    :return: Module
    :rtype: Module
    :return: [description]
    :rtype: [type]
    """

    # Take the last index to avoid edge case where there is another folder named pytorch_toolbox in the whole path
    package_index = [i for i, p in enumerate(path.absolute().parts) if p == package_name][-1]
    module_name = path.stem
    full_module_name = f"{'.'.join(list(path.absolute().parts[package_index:-1]))}.{module_name}"
    module = create_module_from_path(path, module_name=full_module_name)
    return module


def create_module_from_path(path, module_name):
    spec = importlib.util.spec_from_file_location(module_name, str(path))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def create_lookup_from_module(module):
    function_names, function_pointers = load_functions_from_modules(module)
    classes_names, classes_pointers = load_classes_from_modules(module)
    return {name: pointer for (name, pointer) in zip(function_names + classes_names, function_pointers + classes_pointers)}


def load_functions_from_modules(module):
    try:
        function_names, function_pointers = zip(
            *[member for member in inspect.getmembers(module, inspect.isfunction) if member[1].__module__ == module.__name__]
        )
        return function_names, function_pointers
    except ValueError:  # if there are no functions defined
        return (), ()


def load_classes_from_modules(module):
    try:
        class_names, class_pointers = zip(
            *[member for member in inspect.getmembers(module, inspect.isclass) if member[1].__module__ == module.__name__]
        )
        return class_names, class_pointers
    except ValueError:  # if there are no classes defined
        return (), ()


def generate_imports_from_lookup(lookup):
    lookup_with_import_path = {}
    modules_to_be_imported = []
    for name, pointer in lookup.items():
        pointer_module = pointer.__module__
        module_name = pointer_module.split(".")[0]
        lookup_with_import_path[name] = f"{pointer_module}.{name}"
        if module_name not in modules_to_be_imported:
            modules_to_be_imported.append(module_name)
    return lookup_with_import_path, modules_to_be_imported
