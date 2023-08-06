yatte(1) "yatte {{version}}"

# NAME

yatte - a simple task runner

# SYNOPSIS

*yatte* [-h | -V | _task_ [ _task_args_ ... ] ]

# DESCRIPTION

Runs tasks defined in a Python script (named _tasks.py_ by default).

Pass the task name as the first argument, followed by any additional
arguments expected by the task:

	$ *yatte <task> [<task_args> ...]*

Run without arguments to print the list of available tasks and the
arguments expected by each:

	$ *yatte*

# OPTIONS

Use the following flags to display information about the program:

*-h* *--help*
	Show usage information and exit.

*-V* *--version*
	Show the version number and exit.

# EXIT STATUS

Exits with return code *0* upon successful completion, or >= *1* in
case of failure, the exact value depending on the return code of any
subprocesses invoked.

# ENVIRONMENT

The default behaviour can be modified by setting the following
environment variables:

*YATTE_TASKFILE*
	the path to the task file (default: _tasks.py_)

*YATTE_SUCCESS_MSG*
	the message printed to the console upon successful completion of
	the task (default: "= Yatta! =")

# FILES

*yatte* expects the task file to be a Python module containing one or
more function definitions decorated with _yatte.task()_.
See below for an example.

The first line of the function docstring is used as the task
description when printing the task list.

The function can take one or more positional arguments of type _str_,
which must then be supplied on the command line when running the task.

# EXAMPLES

Running *yatte* against this task file:

```
from yatte import task

@task("echo")
def print_echo(word):
    "Echoes a word."
    print(word.upper(), word.title(), word.lower())
```

will produce output like the following:

	$ *yatte*
```
echo word		Echoes a word.
```

	$ *yatte echo hello*
```
HELLO Hello hello
= Yatta! =
```

# SEE ALSO

*invoke*(1) *make*(1)
