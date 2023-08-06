from functools import partial
from pathlib import Path
from tempfile import TemporaryDirectory


def return_boolean(boolean):
    return boolean


def return_negated_boolean(boolean):
    return not boolean


def partially_construct(fn, **kwargs):
    return partial(fn, **kwargs)


def turn_first_arg_into_kwargs(fn):
    def inner_fn(*args, **kwargs):
        return fn(fn=kwargs["fn"], kwargs=args[0])

    return inner_fn


@turn_first_arg_into_kwargs
def spread_arguments_before_call(fn, kwargs):
    return fn(**kwargs)


def function_composer(fns):
    def wrapper(arg):
        for fn in fns:
            arg = fn(arg)
        return arg

    return wrapper


def glob_path(path, glob_string, first_n_paths=None, should_sort=True):
    paths = list(Path(path).glob(glob_string))

    if should_sort:
        paths = sorted(paths)

    if first_n_paths is not None:
        paths = paths[0:first_n_paths]

    return paths


def create_temp_path():
    return TemporaryDirectory().name


lookup = {
    "return_boolean": return_boolean,
    "return_negated_boolean": return_negated_boolean,
    "partially_construct": partially_construct,
    "spread_arguments_before_call": spread_arguments_before_call,
    "function_composer": function_composer,
    "glob_path": glob_path,
    "create_temp_path": create_temp_path,
}
