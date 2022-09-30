import logging
from dataclasses import dataclass

import click
from dicomtrolleytool.logging import get_module_logger
from dicomtrolleytool.persistence import (
    DEFAULT_SETTINGS_PATH,
    DiskSettings,
    KeyRingStorage,
    TrolleyToolSettings,
)

from dicomtrolley.trolley import Trolley

logger = get_module_logger("trolleytool")


@click.group()
@click.option("-v", "--verbose", count=True)
@click.pass_context
def main(ctx, verbose):
    r"""DICOM Trolley tool - DICOM interaction from the command line

    Use the commands below with -h for more info
    """
    configure_logging(verbose)
    ctx.obj = get_context()


def configure_logging(verbose):
    if verbose == 0:
        logging.basicConfig(level=logging.INFO)
        logging.info("Set loglevel to INFO")
    if verbose >= 1:
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Set loglevel to DEBUG")


@dataclass
class TrolleyToolContext:
    trolley: str


def get_context() -> TrolleyToolContext:
    """Collect objects used by trolleytool functions"

    Returns
    -------
    TrolleyToolContext
    """
    return TrolleyToolContext(
        trolley=trolley_from_settings(DiskSettings().get_settings())
    )


def trolley_from_settings(settings: TrolleyToolSettings):
    storage = KeyRingStorage()
    trolley = Trolley(
        searcher=storage.load_channel(settings.searcher_name),
        downloader=storage.load_channel(settings.downloader_name),
    )
    if settings.query_missing:
        trolley.query_missing = settings.query_missing

    return trolley


@click.command(short_help="show tool status")
@click.pass_obj
def status(context: TrolleyToolContext):
    """Get general status of this tool, show currently active server etc."""
    print("Status")
    print(f"Settings file at '{DEFAULT_SETTINGS_PATH}'")
    print(f"trolley: {context.trolley}")


main.add_command(status)
