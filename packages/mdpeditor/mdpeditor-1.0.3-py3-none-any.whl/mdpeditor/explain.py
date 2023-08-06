import rich.markdown
import mdpeditor.mdpblocks.provide as provide
from mdpeditor.parameterhelp import extract


def run_explain(console, explain_string):

    if not explain_string:
        console.print("\nUse as \n\texplain [italic]PARAMETER \n[/]"
                      "where [italic]PARAMETER[/] is "
                      "one of these predefined parameter blocks\n")
        block_names = '\n\t'.join(provide.available_parameter_blocks())
        console.print("[bold]\t" + block_names + "[/]")
        console.print("\nor an .mdp option like [bold]integrator[/].\n")
        return

    explain_string = explain_string.strip()
    try:
        description_as_md = rich.markdown.Markdown(
            extract.mdp_section(explain_string))
        console.print(description_as_md)
        return
    except ValueError as e:
        pass

    try:
        plain_string = provide.description_string(explain_string)
        as_markdown = rich.markdown.Markdown(plain_string)
        console.print(as_markdown)
        return
    except FileNotFoundError as e:
        pass
    except IndexError:
        pass
    except ModuleNotFoundError:
        pass

    raise SystemExit(f"[red bold]{explain_string}[/] is neither an "
                     f".mdp option nor a predefined block")
