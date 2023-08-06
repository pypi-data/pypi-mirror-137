"""Helper functions for use in writing tasks"""
import os
import subprocess
import sys
from concurrent.futures import ProcessPoolExecutor
from logging import error
from pathlib import Path
from shlex import quote
from typing import Iterable, List, Union


def stderr(s: str):
    """Print a string to stderr."""
    print(s, file=sys.stderr)


def run(cmd: Union[str, List[str]]):
    """Run a shell command."""
    if isinstance(cmd, list):
        cmd = " ".join(map(quote, cmd))
        # equivalent to shlex.join() in python >= 3.8

    stderr(f"$ {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        raise SystemExit(e.returncode)


def runp(cmds: Iterable[str]):
    """Run shell commands in parallel."""
    with ProcessPoolExecutor() as executor:
        retcodes = list(executor.map(_run, cmds))

    if any(retcodes):
        raise SystemExit(max(retcodes))


def _run(cmd: str) -> int:
    """Run a shell command and print its output upon completion."""
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    stderr(f"$ {cmd}")

    if p.stdout:
        print(p.stdout.rstrip())

    if p.stderr:
        stderr(p.stderr.rstrip())

    if p.returncode:
        error("Command %r returned non-zero exit status %d.", cmd, p.returncode)

    return p.returncode


def mkdir(d: Path):
    """Create directory d if it doesn't already exist."""
    if not d.is_dir():
        run(["mkdir", "-p", str(d)])


def cp(src: Path, dest: Path):
    """Copy src to dest if dest doesn't already exist."""
    if not dest.is_file():
        mkdir(dest.parent)
        run(["cp", "-p", str(src), str(dest)])


def is_newer(f: Path, than: Path) -> bool:
    """Return True if f exists and is newer than the second argument."""
    return f.is_file() and f.stat().st_mtime > than.stat().st_mtime


def check_envvars(names: set) -> set:
    """Return the environment variables in names that are undefined."""
    return names - set(os.environ)
