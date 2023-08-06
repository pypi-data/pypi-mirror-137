import argparse
import inspect
import sys
import typing
import warnings

import coloring


class ArgparseSubcmdHelper:
    """argparse class Helper for making subcommands easily
    To add a subcommand x implement the following methods/attributes
        def parser_x(self, parser): add arguments to the subcommand parser
        def run_x(self, args):  run the subcommand
        description_x: description of the subcommand


    cls attributes
        prog:
        _parser_main: add to the main parser
        _run_main(self, args): hook after parsing args, handling main variable before dispatch to subcmd

    Custom help
        groups

    Nested subcommand
        command_x: of Type[ArgparseSubcmdHelper]


    """

    prog = None
    description = None
    groups = None  # FIXME: not yet correctly implemented/tested

    # TODO: add a way to have an optional subcm (dont thtrow and error when called withotu subcmd)
    # TODO: improve the custom help! and test it
    def _parser_main(self, parser):
        """Hook to add arguments to the main parser (general arguments)"""
        pass

    def _run_main(self, args):
        """Hook to execute code before executing the subcommand"""
        pass

    def _init_help(self):
        """If groups exist change the current help"""
        # FIXME: imlement/test me
        if not self.groups:
            return
        SPACES = "    "
        color_help = getattr(self, "color_help", False)
        # header prog name and description
        prog = self.prog or sys.argv[0]
        help = f"usage: {prog} [-h] <subcommand>\n\n"

        if self.description:
            help += f"{self.description}\n\n"

        # get the longest command name for pretty print with tabulations
        # flatten all commands names in self.groups()
        grouped_commands_name = [
            cmd for e in self.groups.values() for cmd in e.get("commands", [])
        ]
        all_commands_name = [e[4:] for e in dir(self) if e.startswith("run_")]
        # TODO: add nested commands
        ungrouped_printed_commands = [
            e for e in all_commands_name if e not in grouped_commands_name
        ]
        # max command length for pretty print (aligned)
        max_command_length = len(max(grouped_commands_name, key=len))
        # FIXME: check that ungrouped do not exist
        # add ungrouped commands
        if ungrouped_printed_commands:
            self.groups["ungrouped"] = {
                "commands": ungrouped_printed_commands,
                "title": "Other commands",
                # "description": "commands that do not belong to any group",
            }

        for group_name, group in self.groups.items():
            group_title = group.get("title", group_name) + ":"
            if color_help:
                group_title = coloring.colorize(group_title, c="slate_blue3", s="b")
            commands = group["commands"]
            group_description = group.get("description", "")

            help += group_title
            if group_description:
                help += " " + group_description
            help += "\n\n"
            for cmd in commands:
                # check if the command exist!
                if not hasattr(self, f"run_{cmd}"):
                    raise TypeError(
                        f"Command {cmd!r} can't be in a group because it don't exist (consider implementing 'run_{cmd}')"
                    )
                description_command = getattr(self, f"description_{cmd}", "")
                cmd_txt = cmd.ljust(max_command_length)
                if color_help:
                    cmd_txt = coloring.colorize(cmd_txt, c="medium_purple")
                help += f"{SPACES}{cmd_txt}{SPACES} {description_command}\n"
            help += "\n"

        # change the help function
        self.parser.print_help = lambda file=None: print(help, file=file)
        # self.main_parser.print_usage = self.main_parser.print_help

    def __init__(self, parser=None, subcommand_depth=1):
        # subcommand_depth to allow different level of subcommands and have
        #   the correct dest for subcommands "subcommand" "subcommand_2" "subcommand_3" ...
        self.subcommand_depth = subcommand_depth

        # create main parser
        if parser is None:
            parser = argparse.ArgumentParser(
                prog=self.prog, description=self.description
            )
        self.parser = parser

        # hook to add arguments for the main program
        self._parser_main(self.parser)
        self._build_command()

    def _build_command(self):
        # init the subcommande
        if self.subcommand_depth == 1:
            dest = "subcommand"
        else:
            dest = f"subcommand_{self.subcommand_depth}"

        self.subparsers = self.parser.add_subparsers(dest=dest)
        # Handle all the run_<x> commands
        for subcommand_name in [
            e[len("run_") :] for e in dir(self) if e.startswith("run_")
        ]:
            # Check that the subcommand is callable
            if not callable(getattr(self, "run_" + subcommand_name)):
                raise TypeError(f"Attrbute {'run_'+subcommand_name} must be callable")

            # check that command_<x> and run_<x> dont exist
            if hasattr(self, f"command_{subcommand_name}"):
                raise RuntimeError(
                    f"Both command_{subcommand_name} and run_{subcommand_name} are present"
                )

            # get help if exist
            description = getattr(self, "description_" + subcommand_name, None)
            subparser = self.subparsers.add_parser(
                subcommand_name, help=description, description=description
            )
            parser_name = f"parser_{subcommand_name}"

            # add parser_<cmd> if exist (the parser_<cmd> is not required only run_<cmd> is)
            if hasattr(self, parser_name):
                parser_func = getattr(self, parser_name)
                parser_func(subparser)

        # If parser_x exist but run_x don't raise an exception
        for parser_name in [
            e[len("parser_") :] for e in dir(self) if e.startswith("parser_")
        ]:
            if not hasattr(self, "run_" + parser_name):
                raise RuntimeError(
                    f"parser_{parser_name} method present but run_{parser_name} missing"
                )

        # change help if groups attribute is present
        self._init_help()

        # handle all the command_<x> subcommands
        for subcommand_name in [
            e[len("command_") :] for e in dir(self) if e.startswith("command_")
        ]:
            subcommand_cls: typing.Type[ArgparseSubcmdHelper] = getattr(
                self, "command_" + subcommand_name
            )
            if (not inspect.isclass(subcommand_cls)) or not (
                issubclass(subcommand_cls, ArgparseSubcmdHelper)
            ):
                raise TypeError(
                    f"command_{subcommand_name} attribute must be a class that inherit from {ArgparseSubcmdHelper.__name__!r} not '{type(subcommand_name).__name__}'"
                )

            subcmd_description = getattr(self, f"description_{subcommand_name}", None)
            # TODO: add help_ and description_
            subcmd_parser = self.subparsers.add_parser(
                subcommand_name, description=subcmd_description, help=subcmd_description
            )
            subcommand = subcommand_cls(
                parser=subcmd_parser, subcommand_depth=self.subcommand_depth + 1
            )
            setattr(self, f"_instance_command_{subcommand_name}", subcommand)

    def parse_args(self, args=None):
        return self.parser.parse_args(args)

    def run(self, args=None):
        """Run the main program"""
        parsed_args = self.parser.parse_args(args)
        self._run_main(parsed_args)  # hook to _run_main
        self._run(self, parsed_args)

    def _run(self, command, parsed_args, depth=1):
        """Search the subfunction to run recursivly"""
        if depth == 1:
            subcommand_name_attribute = "subcommand"
        else:
            subcommand_name_attribute = f"subcommand_{depth}"

        subcommand_name = getattr(parsed_args, subcommand_name_attribute)
        if subcommand_name is None:
            command.parser.print_help()
            sys.exit(1)

        if hasattr(command, f"run_{subcommand_name}"):
            subcommand = getattr(command, f"run_{subcommand_name}")
            subcommand(parsed_args)
        elif hasattr(command, f"command_{subcommand_name}"):
            subcommand_instance = getattr(
                command, f"_instance_command_{subcommand_name}"
            )
            self._run(subcommand_instance, parsed_args, depth + 1)

    def main(self, *args, **kwargs):
        """Deprecated run method"""
        warnings.warn(
            "main will be deprecated in future version, use run instead",
            PendingDeprecationWarning,
        )
        self.run(*args, **kwargs)
