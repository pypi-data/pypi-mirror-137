import rich.markdown

import mdpeditor.mdpblocks.provide
import mdpeditor.parameterhelp


def help_explain_string(predefined_blocks):
    help_string = ("Use as [italic]explain PARAMETER[/] "
                   "where [italic]PARAMETER[/] is "
                   "\n - an .mdp option like [bold]integrator[/] or "
                   "\n - one of these predefined parameter blocks")

    help_string += ("\n[bold]" + predefined_blocks + "[/]\n")

    help_string += ("\nExamples:"
                    "\n\t[italic]explain density_guided.vanilla"
                    "\n\t[italic]explain integrator\n")

    return help_string


def run_explain(explain_string):

    if not explain_string or explain_string.strip() == "help":
        return help_explain_string(
            mdpeditor.mdpblocks.provide.available_parameter_blocks())

    explain_string = explain_string.strip()
    try:
        return rich.markdown.Markdown(
            mdpeditor.parameterhelp.extract.mdp_section(explain_string))
    except ValueError as e:
        pass

    try:
        plain_string = mdpeditor.mdpblocks.provide.description_string(
            explain_string)
        return rich.markdown.Markdown(plain_string)

    except FileNotFoundError as e:
        pass
    except IndexError:
        pass
    except ModuleNotFoundError:
        pass

    raise SystemExit(f"[bold]{explain_string}[/] is neither an "
                     f".mdp option nor a predefined block")
