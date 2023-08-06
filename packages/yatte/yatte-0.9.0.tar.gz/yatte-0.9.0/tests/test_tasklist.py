import re

import pytest

from yatte.tasklist import ArgCountError, Task, TaskList, task


def f1():
    """Task 1

    This line will not be displayed.
    """
    print("Running t1")


def f2(a, b):
    """Task 2"""
    print("Running t2 with", a, "and", b)


def test_empty_tasklist():
    tl = TaskList()
    assert len(tl) == 0
    assert str(tl) == "<No tasks defined>"


def test_creating_tasks():
    t1 = Task("first", f1)
    t2 = Task("second", f2)

    assert re.fullmatch(r"first\s+Task 1", str(t1)) is not None
    assert re.fullmatch(r"second a b\s+Task 2", str(t2)) is not None

    tl = TaskList()
    assert list(tl.items()) == [("first", t1), ("second", t2)]
    assert str(tl) == str(t1) + "\n" + str(t2)


def test_creating_tasks_via_wrapper():
    t1 = task("first")(f1)
    t2 = task("second")(f2)
    assert t1.name == "first" and t1.fn == f1

    tl = TaskList()
    assert list(tl.items()) == [("first", t1), ("second", t2)]


def test_running_tasks(capsys):
    task("first")(f1)
    t2 = Task("t2", f2)

    tl = TaskList()
    tl["first"]()
    assert capsys.readouterr().out == "Running t1\n"

    with pytest.raises(ArgCountError):
        t2("x")

    t2("x", 1)
    assert capsys.readouterr().out == "Running t2 with x and 1\n"
