"""Taskfile loader"""
import importlib.util
from os.path import exists, isfile, realpath


class TaskfileImportError(ImportError):
    """Taskfile can't be imported as a Python module.

    Used to distinguish failure to import a non-python file
    from `ImportError`s raised by an otherwise valid taskfile.
    """

    pass


def load_taskfile(path: str):
    """Load the tasks from the given file.

    Nothing is returned but the tasks are registered on the `Task` class
    and can be accessed by instantiating `TaskList`.

    Raises:
    `FileNotFoundError` if `path` is not an existent path;
    `ValueError` if the path exists but is not a file; or
    `TaskfileImportError` if the file can't be parsed as a Python module.

    Apart from the error handling, it was copied straight from:
    https://docs.python.org/3/library/importlib.html#importing-a-source-file-directly
    """
    # spec_from_file_location() seems to only raise a FileNotFoundError
    # for nonexistent files if the path ends in .py, so check explicitly
    # in order to provide informative error messages.
    if not exists(path):
        raise FileNotFoundError(f"File {realpath(path)!r} not found")

    if exists(path) and not isfile(path):
        raise ValueError(f"Can't import tasks from {path!r}: it is not a file")

    spec = importlib.util.spec_from_file_location("task_specs", path)
    if spec is None:
        raise TaskfileImportError(f"Failed to import {path!r} as a Python module")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore

    # Note: The module doesn't need to be added to `sys.modules`,
    # since it won't actually be imported by name / import path.
