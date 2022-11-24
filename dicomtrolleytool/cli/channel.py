import click

from dicomtrolleytool.cli.cli_core import TrolleyToolContext


@click.group()
@click.pass_obj
def channel():
    """Manage ways of querying and retrieving DICOM data"""


@click.command(short_help="Show all channels", name="list")
@click.pass_obj
def cli_list(context: TrolleyToolContext):
    """Show all channels"""
    print("Channels:")
    print(f"{context.settings.channels}")


channel.add_command(cli_list)
