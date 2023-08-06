from rich.console import Console

import mdpeditor.parameterhandler as parameterhandler
import mdpeditor.mdpblocks.provide


def help_compile_string(blocks):

    help = ("[italic]compile[/] helps you to put together your .mdp file with"
            " these predefined blocks:")

    help += ("\n[bold]" + blocks + "[/]\n")

    help += ("\nUse [italic]explain[/] instead of [italic]compile[/] to "
             "learn more about these blocks.\n")

    help += "\nExamples:\n"
    help += (
        "\n\t[italic]compile density_guided.vanilla pixel-size-in-nm=0.98 "
        "reference-density-filename=map.mrc some.mdp"
        "\n\tcompile --merge-duplicates force_field.amber "
        "pressure.atomspheric[/]\n")

    return help


def run_compile(compile_command, merge_right, full_mdp):

    # print some hints if the input string is empty
    if not compile_command or compile_command[0].strip() == "help":
        return help_compile_string(
            mdpeditor.mdpblocks.provide.available_parameter_blocks())

    try:
        output_parameters = parameterhandler.compile_parameters(
            compile_command)
    except ValueError as e:
        raise SystemExit(e.__str__())
    except AttributeError as e:
        raise SystemExit()

    if (not merge_right and output_parameters.duplicate_keys):
        raise SystemExit(
            "\nAborting compilation due to duplicate parameter(s)\n\n\t" +
            "\n\t".join(list(output_parameters.duplicate_keys)) +
            "\n\nUse --merge-duplicates to override parameters\n")

    if not full_mdp:
        # discard all parameters that were not explicitely chosen
        output_parameters.keep_only_modified()

    return output_parameters.as_string()


def print_annotated_output(console, output_string, version, arguments,
                           output_file):

    # keep track of the command used to generate
    # the output by prepending a commented line
    prefix = f"; Created by mdpeditor version {version}\n;"
    prefix += ' '.join(arguments)
    prefix += ("\n; To create self-documenting workflows, do not edit this"
               " file but rerun this tool with different settings\n")

    # direct output to outputfile
    if output_file:
        console = Console(file=output_file)

    console.print(prefix + output_string, style="")
