import click

from dicomtrolleytool.cli.channel import channel
from dicomtrolleytool.cli.cli_core import (
    TrolleyToolContext,
    configure_logging,
    get_context,
)
from dicomtrolleytool.cli.query import query
from dicomtrolleytool.persistence import (
    DEFAULT_SETTINGS_PATH,
)


@click.group()
@click.option("-v", "--verbose", count=True)
@click.pass_context
def main(ctx, verbose):
    r"""DICOM Trolley tool - DICOM interaction from the command line

    Use the commands below with -h for more info
    """
    configure_logging(verbose)
    ctx.obj = get_context()


@click.command(short_help="show tool status")
@click.pass_obj
def status(context: TrolleyToolContext):
    """Get general status of this tool, show currently active server etc."""
    print("Status")
    print(f"Settings file at '{DEFAULT_SETTINGS_PATH}'")
    print(f"trolley: {context.trolley}")


@click.group
def settings():
    """Trolley tool settings"""
    pass


@click.command(short_help="Edit settings")
def edit():
    click.launch(str(DEFAULT_SETTINGS_PATH))


settings.add_command(edit)


main.add_command(status)
main.add_command(channel)
main.add_command(settings)
main.add_command(query)
