import shutil
import sys
from logging import warning

from yatte import task
from yatte.utils import run, runp


@task("setup")
def setup():
    "Set up development environment."
    install_dependencies()
    run("flit install -s")


@task("deps")
def install_dependencies():
    "Install development dependencies."
    run("pip install -r requirements.txt")
    check_installed("scdoc")


@task("typecheck")
def check_types():
    """Run type checker."""
    run("mypy .")


@task("lint")
def run_linters():
    """Run linters."""
    cmds = [
        "isort --check .",
        "black --check .",
        "flake8 .",
    ]
    runp(cmds)


@task("test")
def run_tests():
    """Run tests."""
    run("pytest -q .")


@task("check")
def check():
    """lint + typecheck + test"""
    cmds = [
        "isort --check .",
        "black --check .",
        "flake8 .",
        "mypy .",
        "pytest -q .",
    ]
    runp(cmds)


@task("fmt")
def format():
    """Run formatters."""
    run("isort .")
    run("black .")


sys.path.insert(0, "docs")
import doctasks  # type: ignore  # noqa: E402 F401


@task("upload")
def pypi():
    """Publish package to PyPI."""
    run("flit publish")


@task("clean")
def clean():
    """Remove build/test artefacts."""
    run("rm -rf .mypy_cache")
    run("rm -rf .pytest_cache")
    run("rm -rf dist")
    run("rm -rf docs/_built")


# Helper functions


def check_installed(cmd: str):
    if shutil.which(cmd) is None:
        warning("%r is required for some tasks but is not installed.", cmd)
