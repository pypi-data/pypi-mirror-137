import readline
import mdpeditor.mdpblocks.provide
import mdpeditor.mdpblocks.process
import mdpeditor.compile
import mdpeditor.explain
import mdpeditor.parameterhelp.extract
import time


class Completer:
    def __init__(self, blocks, parameter_keys):
        self.blocks = blocks
        self.parameter_keys = parameter_keys

    def complete_compile(self, text, state):
        """ add a = for parameters tab completion
        """
        results = [
            x + " " for x in self.blocks if x.startswith(text)] + [
            x + "=" for x in self.parameter_keys if x.startswith(text)
        ] + [None]
        return results[state]

    def complete_explain(self, text, state):
        results = [
            x + " " for x in self.blocks if x.startswith(text)] + [
            x + " " for x in self.parameter_keys if x.startswith(text)
        ] + [None]
        return results[state]


def console_prompt_string(compile_mode):
    modes = ["compile", "explain"]

    if compile_mode:
        modes.reverse()

    console_prompt_string = ("\nPress [bold][ENTER][/bold] to switch to " +
                             f"{modes[0]}" + " mode.\n")
    console_prompt_string += (
        "Press [bold][TAB][/bold] to list input options.\n")
    console_prompt_string += ("Press [bold][CTRL]+C[/bold] to exit, type "
                              "[bold]help[/] for more details on usage.")

    console_prompt_string += f"\n> [bold]{modes[1]}[/] "

    if compile_mode:
        console_prompt_string += "[italic]--merge-duplicates[/] "

    return console_prompt_string


def run_interactive_prompt(console, version):

    simple_text_style = "color(6)"

    # introductory message
    console.rule(f"mdpeditor {version}", style="")
    console.print(
        "Welcome to the interactive mode of mdpeditor!"
        "\n\nHere you"
        " can learn about .mdp parameters and parameter blocks "
        "and test different parameter combinations.\n\nFor production"
        " code in workflows, copy paste the prompt below like [bold]"
        "mdpeditor compile ... [/]"
        " and have a look at [bold]mdpeditor --help[/].\n",
        style=simple_text_style)

    # set up tab completion
    readline.parse_and_bind("tab: complete")
    readline.set_completer_delims(" ")
    blocks = mdpeditor.mdpblocks.provide.available_parameter_blocks()
    mdp_options = mdpeditor.parameterhelp.extract.mdp_options_list()
    completer = Completer(
        blocks,
        mdp_options + mdpeditor.mdpblocks.process.tab_completion_hints())
    readline.set_completer(completer.complete_compile)

    merge_right = True
    full_mdp = False

    line = ""
    compile_mode = False
    while line is not None or line == "end":
        # swap mode if only [Enter] was pressed
        # alter tab completion
        if line == "":
            compile_mode = not compile_mode
            if compile_mode:
                readline.set_completer(completer.complete_compile)
            else:
                readline.set_completer(completer.complete_explain)

        try:
            console.rule(style="")
            line = console.input(console_prompt_string(compile_mode))
            if line == "":
                continue
            if compile_mode:
                output = mdpeditor.compile.run_compile(line.split(),
                                                       merge_right, full_mdp)
            else:
                output = mdpeditor.explain.run_explain(line)
            console.rule()
            console.print(output)

        # end gracefully when the user interrupts
        except KeyboardInterrupt:
            line = None
        except EOFError:
            line = None
        # do not exit like we do when running pure command line mode
        except SystemExit as e:
            console.print(e.__str__() + "\n", style=simple_text_style)

    console.print("\n\nThanks for using mdpeditor!")

    console.print(
        "\nDiscuss .mdp parameters at "
        "https://gromacs.bioexcel.eu/tag/mdp-parameters",
        justify="right")

    console.print(
        "Report issues and suggestions for mdpeditor at "
        "https://gitlab.com/cblau/mdpeditor/-/issues",
        justify="right")

    console.print("\n:Copyright: 2021,2022  Christian Blau", justify="right")
