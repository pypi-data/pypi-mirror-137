import subprocess as sp

import pytest


def test_default_taskfile(capfd):
    sp.run(["yatte", "-h"])
    std = capfd.readouterr()
    assert 'path to the task file (currently: "tasks.py")' in std.out


def test_set_taskfile_via_envvar(capfd, monkeypatch):
    task_file = "Taskfile"
    monkeypatch.setenv("YATTE_TASKFILE", task_file)
    sp.run(["yatte", "-h"])
    std = capfd.readouterr()
    assert f'path to the task file (currently: "{task_file}")' in std.out


def test_set_success_msg_via_envvar(capfd, monkeypatch):
    monkeypatch.setenv("YATTE_SUCCESS_MSG", "<success>")
    sp.run(["yatte", "-h"])
    std = capfd.readouterr()
    assert 'the task (currently: "<success>")' in std.out


def can_print_help(capfd):
    sp.run(["yatte", "-h"])
    std = capfd.readouterr()
    return std.out.startswith("usage: yatte")


def test_taskfile_invalid_path(capfd, monkeypatch):
    monkeypatch.setenv("YATTE_TASKFILE", "/lib")
    sp.run(["yatte"])
    std = capfd.readouterr()
    assert std.err.startswith("ERROR")
    assert "not a file" in std.err

    assert can_print_help(capfd)


def test_taskfile_not_a_python_module(capfd, monkeypatch):
    monkeypatch.setenv("YATTE_TASKFILE", "README.md")
    sp.run(["yatte"])
    std = capfd.readouterr()
    assert std.err.startswith("ERROR: Failed to import")

    assert can_print_help(capfd)


@pytest.fixture
def task_file(monkeypatch, tmp_path):
    f = tmp_path / "tasks.py"
    monkeypatch.setenv("YATTE_TASKFILE", str(f))
    return f


def test_nonexistent_taskfile(capfd, task_file):
    sp.run(["yatte"])
    std = capfd.readouterr()
    assert std.err.startswith("ERROR")
    assert f"'{task_file}' not found" in std.err

    assert can_print_help(capfd)


def test_taskfile_with_errors(capfd, task_file):
    task_file.write_text("import antimatter")

    sp.run(["yatte"])
    std = capfd.readouterr()
    assert std.err.startswith("Traceback")
    assert "No module named 'antimatter'" in std.err

    assert can_print_help(capfd)


def test_empty_taskfile(capfd, task_file):
    task_file.touch()

    sp.run(["yatte"])
    std = capfd.readouterr()
    assert std.err == ""
    assert std.out == "<No tasks defined>\n"

    assert can_print_help(capfd)


task_def = """from yatte import task
@task('test')
def test(s):
    "Print s"
    print(s)
"""


def test_taskfile_with_one_task(capfd, monkeypatch, task_file):
    task_file.write_text(task_def)
    monkeypatch.setenv("YATTE_SUCCESS_MSG", "<success>")

    sp.run(["yatte"])
    std = capfd.readouterr()
    assert std.out.split(maxsplit=2) == ["test", "s", "Print s\n"]

    sp.run(["yatte", "fix"])
    std = capfd.readouterr()
    assert std.err.startswith("ERROR: Task 'fix' not defined")
    assert std.err.endswith("choose from { test }\n")

    sp.run(["yatte", "test"])
    std = capfd.readouterr()
    assert std.err.startswith("ERROR: Wrong number of arguments")
    assert "Usage:\n\ttest s" in std.err

    sp.run(["yatte", "test", "hi"])
    std = capfd.readouterr()
    assert std.out == "hi\n"
    assert std.err == "<success>\n"

    sp.run(["yatte", "test", "hi", "there"])
    std = capfd.readouterr()
    assert std.err.startswith("ERROR: Wrong number of arguments")
