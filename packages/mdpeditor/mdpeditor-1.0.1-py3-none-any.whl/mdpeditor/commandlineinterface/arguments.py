import argparse
import sys

from mdpeditor.mdpblocks import provide


def add_explain_subparser(subparsers):
    explain_parser = subparsers.add_parser("explain")

    explain_parser.add_argument(
        dest="explain",
        nargs='?',
        metavar="explain",
        help="explain an .mdp parameter or parameter block",
    )


def add_compile_subparser(subparsers):

    compile_parser = subparsers.add_parser("compile")

    compile_parser.add_argument(dest="compile",
                                nargs="*",
                                metavar="compile tokens")

    compile_parser.add_argument(
        "--merge-duplicates",
        dest="merge_right",
        action='store_true',
        default=False,
        help="allow duplicate parameters by overwriting previously set"
        " parameters")

    compile_parser.add_argument(
        "--output",
        nargs='?',
        const='compiled.mdp',
        type=argparse.FileType('w'),
        help="write the compiled parameters to an .mdp file"
        " (instead of command line)",
        metavar="compiled.mdp")

    compile_parser.add_argument("--full-mdp",
                                dest="full_mdp",
                                action='store_true',
                                default=False,
                                help="write all mdp options"
                                "including defaults")


def get_command_line_arguments(version: str):
    """build, parse and return command line arguments

    Args:
        version (str): the current program version

    Returns:
        the parsed command line arguments
    """

    program_name = "mdpeditor"
    description = (
        "Compiles an .mdp file from preset .mdp parameter blocks"
        " and user settings. To learn more about available parameters"
        " use explain. ")

    epilog = """examples:
    mdpeditor explain
    \tShows available pre-defined parameter blocks

    mdpeditor compile force_field.charmm nsteps=100
    \tCompiles the pre-defined block force_field.charmm and
    \tsets "nsteps = 100" in the output
    """

    parser = argparse.ArgumentParser(
        description=description,
        prog=program_name,
        add_help=False,
        epilog=epilog,
        formatter_class=argparse.RawDescriptionHelpFormatter)

    subparsers = parser.add_subparsers(help='', dest='command')

    parser.add_argument("-h",
                        "--help",
                        action="help",
                        help="show this help message and exit")

    parser.add_argument("--version",
                        action="version",
                        version=(f"{program_name} {version}"))

    add_compile_subparser(subparsers)
    add_explain_subparser(subparsers)

    return parser.parse_args()
