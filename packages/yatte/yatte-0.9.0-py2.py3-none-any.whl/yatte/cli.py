"""Command-line interface for running tasks"""
import logging
from argparse import ArgumentParser, Namespace, RawDescriptionHelpFormatter
from logging import error
from os import getenv
from textwrap import dedent

from . import __version__
from .taskfile import TaskfileImportError
from .tasklist import ArgCountError, TaskList
from .utils import stderr

TASKFILE_ENVVAR = "YATTE_TASKFILE"
SUCCESS_MSG_ENVVAR = "YATTE_SUCCESS_MSG"

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def parse_args() -> Namespace:
    """Sets up the CLI and returns the arguments provided by the user."""
    ns = Namespace()
    ns.task_file = getenv(TASKFILE_ENVVAR, "tasks.py")
    ns.success_msg = getenv(SUCCESS_MSG_ENVVAR, "= Yatta! =")

    usage = "%(prog)s [-h | -V | task [task_args...]]"

    description = dedent(
        f"""
    Runs tasks defined in a `{ns.task_file}` file.

    The task file must be a Python module containing one or more
    function definitions decorated with `@task`, e.g.:

        from yatte import task

        @task("echo")
        def print_echo(word):
            "Echoes a word."
            print(word.upper(), word.title(), word.lower())

    Run without arguments to print the list of available tasks
    and the arguments expected by each:

        $ %(prog)s
        echo word       Echoes a word.

    To run a task, pass its name as the first argument,
    followed by its required arguments.

        $ %(prog)s echo hello
        HELLO Hello hello
        {ns.success_msg}
    """
    )

    epilog = dedent(
        f"""
    The default behaviour can be modified by setting the
    following environment variables:

    {TASKFILE_ENVVAR}
        the path to the task file (currently: "{ns.task_file}")

    {SUCCESS_MSG_ENVVAR}
        the message printed to the console upon successful
        completion of the task (currently: "{ns.success_msg}")

    %(prog)s exits with return code of 0 upon successful
    completion, or >= 1 in case of failure, the exact value
    depending on the return code of any subprocesses invoked.
    """
    )
    parser = ArgumentParser(
        usage=usage,
        description=description,
        epilog=epilog,
        formatter_class=RawDescriptionHelpFormatter,
    )
    parser.add_argument("task", nargs="?")
    parser.add_argument("task_args", nargs="*")
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser.parse_args(namespace=ns)


def main():
    """The entry point for the console script

    Loads the tasks from the task file and either
    runs the requested task with the given arguments, or
    prints the task descriptions if no task was requested.
    """
    args = parse_args()

    try:
        tasks = TaskList.load_from(args.task_file)
    except (FileNotFoundError, ValueError, TaskfileImportError) as e:
        error(e)
        raise SystemExit(1)
    # Other errors not caught, since the traceback could be useful.

    if args.task is None:
        print(tasks)
        raise SystemExit(0)

    try:
        task = tasks[args.task]
    except KeyError:
        error("Task %r not defined; choose from { %s }", args.task, " ".join(tasks))
        raise SystemExit(1)

    try:
        task(*args.task_args)
    except ArgCountError as e:
        error(e)
        stderr(f"Usage:\n\t{task}")
        raise SystemExit(1)

    stderr(args.success_msg)
