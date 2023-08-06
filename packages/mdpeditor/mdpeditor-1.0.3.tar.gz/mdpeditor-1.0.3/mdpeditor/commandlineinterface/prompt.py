import readline
import mdpeditor.mdpblocks.provide
import mdpeditor.compile
import mdpeditor.explain
import mdpeditor.parameterhelp.extract


class VolcabCompleter:
    def __init__(self, volcab):
        self.volcab = volcab

    def complete(self, text, state):
        results = [x + " " for x in self.volcab if x.startswith(text)] + [None]
        return results[state]


def console_prompt_string(compile_mode):
    modes = ["compile", "explain"]

    if compile_mode:
        modes.reverse()

    console_prompt_string = ("\nPress [bold][ENTER][/bold] to switch to " +
                             f"{modes[0]}" + " mode.\n")
    console_prompt_string += (
        "Press [bold][TAB][/bold] to list input options.\n")
    console_prompt_string += ("Press [bold][CTRL]+C[/bold] to exit.\n")

    console_prompt_string += f"\n> [bold]{modes[1]}[/] "

    if compile_mode:
        console_prompt_string += "[italic]--merge-duplicates[/] "

    return console_prompt_string


def run_interactive_prompt(console, version):

    error_style = "bold color(1)"
    simple_text_style = "color(6)"

    # introductory message
    console.rule(f"mdpeditor {version}", style="")
    console.print(
        "Welcome to the interactive mode of mdpeditor!"
        "\n\nHere you"
        " can learn about .mdp parameters and parameter blocks "
        "and test different parameter combinations.\n\nFor production"
        " code in workflows, use the command line options as shown"
        " when running [italic]mdpeditor --help.\n",
        style=simple_text_style)
    available_blocks = mdpeditor.mdpblocks.provide.available_parameter_blocks()
    console.print("To help you compile your .mdp file, you can currently "
                  "choose from these blocks:\n\n[bold]" +
                  "\n".join(available_blocks),
                  style=simple_text_style)
    console.print(
        "\nLearn more about these blocks with the [bold]explain[/] mode.\n",
        style=simple_text_style)

    console.print(
        "\nA typical input is \n"
        "[italic]compile --merge-duplicates force_field.amber "
        "pressure.atomspheric[/]\n",
        style=simple_text_style)

    # set up tab completion
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" ")
    blocks = mdpeditor.mdpblocks.provide.available_parameter_blocks()
    mdp_options = mdpeditor.parameterhelp.extract.mdp_options_list()
    completer = VolcabCompleter(blocks + mdp_options)
    readline.set_completer(completer.complete)

    merge_right = True
    full_mdp = False

    line = ""
    compile_mode = False
    while line is not None or line == "end":

        # swap mode if only [Enter] was pressed
        if line == "":
            compile_mode = not compile_mode

        try:
            console.rule(style="")
            line = console.input(console_prompt_string(compile_mode))
            if compile_mode:
                if line == "":
                    continue
                output = mdpeditor.compile.run_compile(line.split(),
                                                       merge_right, full_mdp)
                console.print(output)
            else:
                if line == "":
                    continue
                mdpeditor.explain.run_explain(console, line)

        # end gracefully when the user interrupts
        except KeyboardInterrupt:
            line = None
        except EOFError:
            line = None
        # do not exit like we do when running pure command line mode
        except SystemExit as e:
            console.print("Error: " + e.__str__() + "\n", style=error_style)

    console.print("\n\nThanks for using mdpeditor!")

    console.print(
        "\nDiscuss .mdp parameters at "
        "https://gromacs.bioexcel.eu/tag/mdp-parameters", justify="right"
    )

    console.print(
        "Report issues and suggestions for mdpeditor at "
        "https://gitlab.com/cblau/mdpeditor/-/issues",
        justify="right")

    console.print("\n:Copyright: 2021,2022  Christian Blau", justify="right")
