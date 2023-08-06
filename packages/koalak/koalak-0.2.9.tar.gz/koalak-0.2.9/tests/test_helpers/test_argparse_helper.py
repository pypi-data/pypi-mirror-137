import argparse
import shlex

import pytest
from koalak import ArgparseSubcmdHelper


def test_run_cmd(capsys):
    class SimpleCommand(ArgparseSubcmdHelper):
        def parser_mycmd(self, parser):
            pass

        def run_mycmd(self, args):
            print(1)

    simple_command = SimpleCommand()

    # assert that "mycmd" parse
    simple_command.parse_args(["mycmd"])

    capsys.readouterr()  # ignore the first prints
    simple_command.run(["mycmd"])
    captured = capsys.readouterr()
    assert captured.out == "1\n"


def test_run_with_args(capsys):
    class SimpleCommand(ArgparseSubcmdHelper):
        def parser_mycmd(self, parser):
            parser.add_argument("printme")

        def run_mycmd(self, args):
            print(args.printme)

    simple_command = SimpleCommand()

    # assert that "mycmd" parse
    simple_command.parse_args(["mycmd", "1"])

    with pytest.raises(SystemExit):
        simple_command.parse_args(["mycmd"])

    capsys.readouterr()  # ignore the first prints

    simple_command.run(["mycmd", "test"])
    captured = capsys.readouterr()
    assert captured.out == "test\n"

    simple_command.run(["mycmd", "22"])
    captured = capsys.readouterr()
    assert captured.out == "22\n"


def test_run_without_parse():
    """run_x without parse_x should not be a problem"""

    class SimpleCommand(ArgparseSubcmdHelper):
        def run_mycmd(self, args):
            pass

    simple_command = SimpleCommand()
    simple_command.parse_args(["mycmd"])
    simple_command.run(["mycmd"])


def test_parse_without_run():
    """parse_x without run_x should not be a problem"""

    class SimpleCommand(ArgparseSubcmdHelper):
        def parser_mycmd(self, args):
            pass

    # parser_mycmd exist but run_mycmd not present
    with pytest.raises(RuntimeError):
        SimpleCommand()


def test_run_without_subcmd():
    class SimpleCommand(ArgparseSubcmdHelper):
        def run_mycmd(self, args):
            pass

    simple_command = SimpleCommand()
    with pytest.raises(SystemExit):
        simple_command.run([])  # run without any inputs


def test_run_non_existing_cmd():
    class SimpleCommand(ArgparseSubcmdHelper):
        name = "simple"

        def run_mycmd(self, args):
            pass

    simple_command = SimpleCommand()
    with pytest.raises(SystemExit):
        simple_command.run(["dontexist"])


def test_run_attribute_not_callable():
    class SimpleCommand(ArgparseSubcmdHelper):
        run_x = "String and not callable"

    with pytest.raises(TypeError):
        SimpleCommand()


def test_nested_commands(capsys):
    class VarCommand(ArgparseSubcmdHelper):
        def run_ls(self, args):
            print("ls")

        def run_add(self, args):
            print("add")

    class ToolsmanagerCommand(ArgparseSubcmdHelper):
        command_var = VarCommand

        def run_version(self, args):
            print("version")

    toolsmanager_command = ToolsmanagerCommand()

    capsys.readouterr()  # ignore the first prints
    toolsmanager_command.run(["version"])
    captured = capsys.readouterr()
    assert captured.out == "version\n"

    toolsmanager_command.run(["var", "ls"])
    captured = capsys.readouterr()
    assert captured.out == "ls\n"

    toolsmanager_command.run(["var", "add"])
    captured = capsys.readouterr()
    assert captured.out == "add\n"


def test_nested_commands_depth_2(capsys):
    class Depth3Command(ArgparseSubcmdHelper):
        def run_a(self, args):
            print("d3.a")

        def run_b(self, args):
            print("d3.b")

    class Depth2Command(ArgparseSubcmdHelper):
        command_depth = Depth3Command

        def run_a(self, args):
            print("d2.a")

        def run_b(self, args):
            print("d2.b")

    class Depth1Command(ArgparseSubcmdHelper):
        command_depth = Depth2Command

        def run_a(self, args):
            print("d1.a")

        def run_b(self, args):
            print("d1.b")

    command = Depth1Command()

    capsys.readouterr()  # ignore the first prints
    command.run(["a"])
    captured = capsys.readouterr()
    assert captured.out == "d1.a\n"

    capsys.readouterr()  # ignore the first prints
    command.run(["b"])
    captured = capsys.readouterr()
    assert captured.out == "d1.b\n"

    with pytest.raises(SystemExit):
        command.run([])

    # depth2
    capsys.readouterr()  # ignore the first prints
    command.run(["depth", "a"])
    captured = capsys.readouterr()
    assert captured.out == "d2.a\n"

    capsys.readouterr()  # ignore the first prints
    command.run(["depth", "b"])
    captured = capsys.readouterr()
    assert captured.out == "d2.b\n"

    with pytest.raises(SystemExit):
        command.run(["depth"])

    # depth3
    capsys.readouterr()  # ignore the first prints
    command.run(["depth", "depth", "a"])
    captured = capsys.readouterr()
    assert captured.out == "d3.a\n"

    capsys.readouterr()  # ignore the first prints
    command.run(["depth", "depth", "b"])
    captured = capsys.readouterr()
    assert captured.out == "d3.b\n"

    with pytest.raises(SystemExit):
        command.run(["depth", "depth"])

    # None existing commands/args
    with pytest.raises(SystemExit):
        command.run(["a", "dontexist"])

    with pytest.raises(SystemExit):
        command.run(["depth", "dontexist"])

    with pytest.raises(SystemExit):
        command.run(["depth", "depth", "dontexist"])

    with pytest.raises(SystemExit):
        command.run(["a", "-x"])


def test_run_x_and_command_x_error():
    class VarCommand(ArgparseSubcmdHelper):
        pass

    class ToolsmanagerCommand(ArgparseSubcmdHelper):
        command_var = VarCommand

        def run_var(self, args):
            pass

    with pytest.raises(RuntimeError):
        ToolsmanagerCommand()


def test_error_command_x_wrong_type():
    class Command(ArgparseSubcmdHelper):
        # command_x must be a class ArgparseSUbcmdHelper
        command_x = "hello"

    with pytest.raises(TypeError):
        Command()


"""
Tests todo
==========
- more testing with args and run them
- generated help (groups)

"""
