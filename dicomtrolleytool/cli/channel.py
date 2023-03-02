import click

from dicomtrolleytool.cli.base import TrolleyToolContext


@click.group()
def channel():
    """Manage ways of querying and retrieving DICOM data"""


@click.command(short_help="Show all channels", name="list")
@click.pass_obj
def cli_list(context: TrolleyToolContext):
    """Show all channels"""
    print("Channels:")
    print(f"{context.settings.channels}")


@click.command(name="set-searcher")
@click.argument("name", type=str)
@click.pass_obj
def set_searcher(context: TrolleyToolContext, name):
    """Set channel to use for search"""
    context.settings.searcher_name = name
    context.settings.save()
    print(f"Set searcher to '{name}'")


channel.add_command(cli_list)
channel.add_command(set_searcher)
