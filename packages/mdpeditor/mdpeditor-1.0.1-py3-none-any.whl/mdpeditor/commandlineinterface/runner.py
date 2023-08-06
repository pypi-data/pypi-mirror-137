""" Run the command line interface """
import argparse
import importlib.metadata
import itertools
import sys

from mdpeditor.explain import run_explain
import mdpeditor.compile
import mdpeditor.commandlineinterface.prompt
import mdpeditor.commandlineinterface.arguments as arguments

from rich.console import Console
from rich import print


def run():
    """ run the command line interface """

    # set up the console for printing
    console = Console()

    # derive the program version via git
    try:
        version = importlib.metadata.version("mdpeditor")
    except importlib.metadata.PackageNotFoundError:
        version = "Unknown"

    command_line_arguments = arguments.get_command_line_arguments(version)

    if command_line_arguments.command == "compile":
        # print some hints if the input string is empty
        if not command_line_arguments.compile:
            console.print(mdpeditor.compile.help_string())
            sys.exit()

        output_string = mdpeditor.compile.run_compile(
            command_line_arguments.compile, command_line_arguments.merge_right,
            command_line_arguments.full_mdp)

        mdpeditor.compile.print_annotated_output(console, output_string,
                                                 version, sys.argv,
                                                 command_line_arguments.output)

        sys.exit()

    if command_line_arguments.command == "explain":
        try:
            run_explain(console, command_line_arguments.explain)
        except SystemExit as e:
            console.print(e.__str__())
            raise SystemExit("")
        sys.exit()

    if not command_line_arguments.command:
        mdpeditor.commandlineinterface.prompt.run_interactive_prompt(
            console, version)
