import sys
import os
import logging

import click
from toscaparser.tosca_template import ToscaTemplate
from ruamel.yaml.error import YAMLError

from micadoparser.parser import set_template
from micadoparser.exceptions import ValidationError

# Turn off logging
logging.basicConfig(level=100)


@click.command(no_args_is_help=True)
@click.argument(
    "files", nargs=-1, type=click.Path(exists=True, dir_okay=False)
)
@click.option("-v", "--verbose", count=True, help="Increase verbosity")
def main(files, verbose):
    """Attempts to parse a MiCADO ADT

    FILE is the path to a single-file (.yaml) or multi-file (.csar) ADT"""
    error = False
    for file in files:
        click.secho(f"Parsing ", fg="yellow", nl=False)
        click.secho(f"{click.format_filename(file)}...", italic=True, nl=False)
        try:
            tpl = set_template(file)
            click.secho("OK", fg="green", bold=True)
            if verbose:
                _generate_detail(tpl, verbose)
                click.echo()
        except YAMLError as e:
            error = True
            click.secho("Invalid YAML", fg="red", bold=True)
            click.echo(e)
        except ValidationError as e:
            error = True
            click.secho("Invalid ADT", fg="red", bold=True)
            click.echo(e)
        except Exception as e:
            click.secho(
                f"\nUnhandled Exception:\n {type(e)}\n  {e}", fg="bright_red"
            )
    if error:
        sys.exit(1)


def _generate_detail(tpl: ToscaTemplate, verbose: int):
    if tpl.input_path and tpl.input_path.endswith("csar"):
        click.secho("  Archive entrypoint: ", bold=True, nl=False)
        click.echo(os.path.basename(tpl.path))

    click.secho("  Description: ", bold=True, nl=False)
    click.echo(tpl.description)

    click.secho("  Node Templates: ", bold=True, nl=False)
    click.echo(f"{len(tpl.nodetemplates)} nodes...")

    if verbose < 2:
        return

    for node in tpl.nodetemplates:
        click.echo(f"    {node.name}: ", nl=False)
        click.secho(node.type, italic=True)


if __name__ == "__main__":
    main()
