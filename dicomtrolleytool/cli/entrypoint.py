"""Entrypoint for trolley CLI command. All subcommands are connected here."""
import click

from dicomtrolleytool.cli.download import download
from dicomtrolleytool.cli.channel import channel
from dicomtrolleytool.cli.base import (
    configure_logging,
    edit,
    get_context,
    settings,
    status,
)
from dicomtrolleytool.cli.query import query


@click.group()
@click.option("-v", "--verbose", count=True)
@click.pass_context
def main(ctx, verbose):
    r"""DICOM Trolley tool - DICOM interaction from the command line

    Use the commands below with -h for more info
    """
    configure_logging(verbose)
    ctx.obj = get_context()


settings.add_command(edit)


main.add_command(status)
main.add_command(channel)
main.add_command(settings)
main.add_command(query)
main.add_command(download)
