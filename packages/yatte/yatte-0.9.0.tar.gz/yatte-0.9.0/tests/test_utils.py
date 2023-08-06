import pytest

import yatte.utils


def test_run_command_successfully(capfd):
    yatte.utils.run("echo ok")
    std = capfd.readouterr()
    assert std.err == "$ echo ok\n"
    assert std.out == "ok\n"


def test_run_command_with_shell_quoting(capfd, tmp_path):
    d = tmp_path / "a sub>dir"  # special chars, so must be quoted
    yatte.utils.mkdir(d)
    std = capfd.readouterr()
    assert std.err == f"$ mkdir -p '{d}'\n"
    assert d.is_dir()

    f = d / "pyproject.toml"
    yatte.utils.cp("pyproject.toml", f)
    std = capfd.readouterr()
    assert std.err == f"$ cp -p pyproject.toml '{f}'\n"
    assert f.is_file()


def test_run_command_that_errors_out(capfd):
    with pytest.raises(SystemExit) as e:
        yatte.utils.run("echo failure imminent; exit 2")

    assert e.value.code == 2
    std = capfd.readouterr()
    assert std.err == "$ echo failure imminent; exit 2\n"
    assert std.out == "failure imminent\n"


def test_run_commands_in_parallel(capfd):
    yatte.utils.runp(["echo 10; sleep 0.01; echo 11", "echo 20; echo 21"])
    # The sleep call ensures that the first command will finish after the second,
    # so both its status message ("$ cmd") and its output will be reported last,
    # indicating that the commands are not being run serially.
    std = capfd.readouterr()
    assert std.err.splitlines() == [
        "$ echo 20; echo 21",
        "$ echo 10; sleep 0.01; echo 11",
    ]
    assert std.out.splitlines() == ["20", "21", "10", "11"]


def test_run_commands_that_fail_in_parallel(capfd):
    with pytest.raises(SystemExit) as e:
        yatte.utils.runp(["echo error >&2; exit 3", "sleep 0.01; echo ok"])

    assert e.value.code == 3
    std = capfd.readouterr()
    assert std.err.splitlines() == [
        "$ echo error >&2; exit 3",
        "error",
        "$ sleep 0.01; echo ok",
    ]
    assert std.out == "ok\n"
