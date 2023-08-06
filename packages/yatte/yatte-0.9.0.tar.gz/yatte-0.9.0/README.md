# yatte

A simple task runner

Make and Bash are useful tools but the syntax can be tricky,
especially if you're writing Bash inside a Makefile.
And sometimes you need the flexibility and expressivity
of a proper programming language with a standard library.

If you know Ruby, you're probably already familiar with Rake;
and for Python there's Invoke.
But maybe you don't want to invest time in learning a new tool
and its idiosyncracies.

**Yatte** is for when you just want to write a Python script
and get back to work.


## Project links

- [Documentation](https://yatte.javiljoen.net/)
- [Source code](https://git.sr.ht/~javiljoen/yatte/)
- [Bug reports etc.](https://lists.sr.ht/~javiljoen/yatte/)


## Quickstart

Install the package:

    pip install yatte

Create a file named `tasks.py` containing some functions decorated with `@task`:

```python
from subprocess import run
from sys import exit, stderr

from yatte import task

@task("greet")
def hello():
    """Greet the world"""
    print("Hello, world!")

@task("list-files")
def list_files(dir):
    """List the files in the directory"""
    shell(f"ls {dir}")

def shell(cmd):
    print("sh>", cmd, file=stderr)
    p = run(cmd, shell=True)
    if p.returncode:
        exit(p.returncode)
```

Then call `yatte` by itself to list the tasks:

    $ yatte
    greet                   Greet the world
    list-files dir          List the files in the directory

And `yatte {task}` to execute the given task:

    $ yatte list-files .
    sh> ls .
    pyproject.toml README.md tasks.py

See the [docs](https://yatte.javiljoen.net/) for more details.
