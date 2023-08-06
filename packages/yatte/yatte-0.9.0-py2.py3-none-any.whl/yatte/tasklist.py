"""Tasks and task lists"""
from __future__ import annotations

from inspect import getdoc, getfile, signature
from typing import Callable, Dict

from .taskfile import load_taskfile


class Task:
    """A wrapper for a function and its CLI name

    The task description displayed by the CLI is composed of
    the task name and the first line of the function docstring.
    """

    _instances: list[Task] = []

    def __init__(self, name: str, fn: Callable):
        self.name = name
        self.fn = fn

        # Register this instance in the class variable
        # to make it easy to create a TaskList.
        self._instances.append(self)

    def __call__(self, *args):
        if len(args) != len(self.args):
            raise ArgCountError(
                "Wrong number of arguments: "
                f"expected {len(self.args)}; got {len(args)}."
            )

        self.fn(*args)

    def __repr__(self) -> str:
        return f"Task({self.name!r}: <{getfile(self.fn)}>:{self.fn.__qualname__})"

    def __str__(self) -> str:
        arglist = " ".join(self.args)
        signature = f"{self.name} {arglist}"
        return f"{signature:<30} {self.doc}"

    @property
    def args(self) -> tuple[str, ...]:
        """The names of the function parameters"""
        return tuple(signature(self.fn).parameters)

    @property
    def doc(self) -> str:
        """The first line of the function docstring"""
        docstring = getdoc(self.fn) or ""
        return docstring and docstring.splitlines()[0]


class ArgCountError(TypeError):
    """Inappropriate number of arguments."""

    pass


class TaskList(Dict[str, Task]):
    """A mapping of Tasks indexed on task name

    When instantiating this class,
    it will collect all instances of Task existing at that time.
    """

    def __init__(self):
        super().__init__({t.name: t for t in Task._instances})

    def __str__(self) -> str:
        return "\n".join(map(str, self.values())) or "<No tasks defined>"

    @classmethod
    def load_from(cls, task_file: str) -> TaskList:
        """Load Tasks defined in task_file into a TaskList."""
        # Import task_file, registering Tasks in Task._instances.
        load_taskfile(task_file)
        return TaskList()


def task(name: str) -> Callable:
    """A decorator for turning functions into Tasks"""

    def make_task(fn: Callable) -> Task:
        return Task(name, fn)

    return make_task
