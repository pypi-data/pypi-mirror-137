import logging
import os

import click

logger = logging.getLogger(__name__)


def create_mlfoundry_cli():
    """Generates CLI by combining all subcommands into a main CLI and returns in
    Returns:
        function: main CLI functions will all added sub-commands
    """
    _cli = mlfoundry_cli()
    _cli.add_command(ui)
    return _cli


@click.group()
@click.version_option("1.0.0")
def mlfoundry_cli():
    """MlFoundry CLI"""
    click.secho("MlFoundry CLI", bold=True, fg="green")


@mlfoundry_cli.command(
    help="Generate MLFoundry Dashboard",
    short_help="Generate MLFoundry Dashboard",
)
@click.option(
    "-w",
    "--webapp_path",
    type=click.Path(),
    required=False,
    default="",
)
@click.option(
    "-p",
    "--path",
    type=click.Path(exists=True, dir_okay=True, readable=True),
    default=os.path.abspath("."),
)
def ui(path: str, webapp_path: str):
    if webapp_path:
        abs_webapp_path = os.path.abspath(webapp_path)
        basename = os.path.basename(abs_webapp_path)
        extension = basename.split(".")[-1]
        if extension != "py" or not os.path.isfile(abs_webapp_path):
            logger.error(f"Must be a valid python file. Received {webapp_path}")
            return
        os.system(f"mlfoundry_ui start-dashboard -p {path} -w {webapp_path}")
    else:
        os.system(f"mlfoundry_ui start-dashboard -p {path}")


@mlfoundry_cli.command(
    help="Generate Webapp Dashboard",
    short_help="Generate Webapp Dashboard",
)
@click.option(
    "-w",
    "--webapp_path",
    type=click.Path(exists=True, readable=True),
)
def webapp(webapp_path: str):
    os.system(f"mlfoundry_ui webapp -w {webapp_path}")
