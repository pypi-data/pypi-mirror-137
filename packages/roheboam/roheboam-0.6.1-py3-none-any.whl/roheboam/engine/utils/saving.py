import time
from contextlib import contextmanager
from pathlib import Path
from tempfile import NamedTemporaryFile, TemporaryDirectory

import cloudpickle


def create_time_stamped_save_path(root_save_directory):
    current_time = f"{time.strftime('%Y%m%d-%H%M%S')}"
    time_stamped_save_path = Path(root_save_directory) / current_time
    return time_stamped_save_path


@contextmanager
def save_to_temporary_file(save_fn, name=None):
    try:
        if name is not None:
            temp_dir = TemporaryDirectory()
            save_path = Path(temp_dir.name) / name
            save_fn(save_path)
            yield str(save_path)
        else:
            temp_file = NamedTemporaryFile()
            save_fn(temp_file.name)
            yield temp_file.name
    finally:
        pass


def dump_object_to_path(path, object):
    return cloudpickle.dump(object, open(path, "wb"))


lookup = {"create_time_stamped_save_path": create_time_stamped_save_path, "save_to_temporary_file": save_to_temporary_file}
