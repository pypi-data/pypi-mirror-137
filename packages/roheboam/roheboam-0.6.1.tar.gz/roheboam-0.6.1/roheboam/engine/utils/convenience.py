import re
import subprocess
import sys
from pathlib import Path

import numpy as np

from ..logger import logger


def is_listy(x):
    return isinstance(x, (tuple, list, np.ndarray))


def if_none(a, b):
    return b if a is None else a


def camel2snake(name):
    _camel_re1 = re.compile("(.)([A-Z][a-z]+)")
    _camel_re2 = re.compile("([a-z0-9])([A-Z])")
    s1 = re.sub(_camel_re1, r"\1_\2", name)
    return re.sub(_camel_re2, r"\1_\2", s1).lower()


def debug_log_on_call(fn):
    def wrapped(*args, **kwargs):
        logger.debug(f"Called: {fn.__qualname__}")
        return fn(*args, **kwargs)

    return wrapped


def find_nearest_greater_divisible(a, b):
    if a % b == 0:
        return a
    return a + (b - (a % b))


def to_numpy(tensor):
    if isinstance(tensor, np.ndarray):
        return tensor
    return tensor.cpu().detach().numpy()


def is_notebook():
    try:
        from IPython import get_ipython

        shell = get_ipython().__class__.__name__
        if shell == "ZMQInteractiveShell":
            return True  # Jupyter notebook or qtconsole
        elif shell == "TerminalInteractiveShell":
            return False  # Terminal running IPython
        else:
            return False  # Other type (?)
    except NameError:
        return False
    except ModuleNotFoundError:
        return False


def git_commit_hash():
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).strip().decode()


def run_shell_command(cmd, silent=False, same_process=False):
    try:
        if not silent:
            print(cmd)
        if same_process:
            process = subprocess.Popen(["bash"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
            process.stdin.write(cmd.encode(sys.stdout.encoding))
            output, _ = process.communicate()
        else:
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            if not silent:
                # output, _ = process.communicate()
                # print(output)
                # sys.stdout.write(output.decode(sys.stdout.encoding))
                for line in iter(process.stdout.readline, b""):
                    sys.stdout.write(line.decode(sys.stdout.encoding))
    except subprocess.CalledProcessError as e:
        print(e.output.decode())


def catch_all_exceptions(fn):
    def wrapped(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except Exception as e:
            logger.warning(f"Exception: {str(e)} for {fn} ignored")

    return wrapped


def class_path_with_default(keys, c, default=None):
    try:
        return class_path(keys, c)
    except KeyError:
        return default


def class_path(keys, c):
    if not keys:
        raise ValueError("Expected at least one key, got {0}".format(keys))
    current_value = c
    for key in keys:
        current_value = getattr(current_value, key)
    return current_value


def remove_path(path: Path):
    if path.is_file() or path.is_symlink():
        path.unlink()
        return
    for p in path.iterdir():
        remove_path(p)
    path.rmdir()


from functools import wraps
from time import time


def timing(f, label=None):
    @wraps(f)
    def wrapper(*args, **kwargs):
        start = time()
        result = f(*args, **kwargs)
        end = time()
        if label:
            print(label)
        print(f"Elapsed time: {end - start}")
        return result

    return wrapper


def get_open_port():
    import socket

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("", 0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port


lookup = {
    "is_listy": is_listy,
    "if_none": if_none,
    "camel2snake": camel2snake,
    "debug_log_on_call": debug_log_on_call,
    "find_nearest_greater_divisible": find_nearest_greater_divisible,
    "to_numpy": to_numpy,
    "is_notebook": is_notebook,
    "catch_all_exceptions": catch_all_exceptions,
    "remove_path": remove_path,
    "timing": timing,
    "get_open_port": get_open_port,
}
