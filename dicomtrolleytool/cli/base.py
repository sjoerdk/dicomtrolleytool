"""Shared objects for CLI and basic CLI commands"""
import logging
from dataclasses import dataclass

import click
from dicomtrolley.trolley import Trolley

from dicomtrolleytool.logs import get_module_logger
from dicomtrolleytool.persistence import (
    DEFAULT_SETTINGS_PATH,
    SettingsFile,
    KeyRingStorage,
    TrolleyToolSettings,
)

logger = get_module_logger("trolleytool")


def configure_logging(verbose):
    if verbose == 0:
        logging.basicConfig(level=logging.INFO)
        logging.info("Set loglevel to INFO")
    if verbose >= 1:
        logging.basicConfig(level=logging.DEBUG)
        logging.info("Set loglevel to DEBUG")


@dataclass
class TrolleyToolContext:
    settings: TrolleyToolSettings
    trolley: Trolley


def get_context() -> TrolleyToolContext:
    """Collect objects used by trolleytool functions"

    Returns
    -------
    TrolleyToolContext
    """
    settings = SettingsFile(path=DEFAULT_SETTINGS_PATH).load_settings()
    return TrolleyToolContext(
        settings=settings, trolley=trolley_from_settings(settings)
    )


def trolley_from_settings(settings: TrolleyToolSettings):
    storage = KeyRingStorage()
    trolley = Trolley(
        searcher=storage.load_channel(settings.searcher_name).init_searcher(),
        downloader=storage.load_channel(settings.downloader_name).init_downloader(),
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


@click.group
def settings():
    """Trolley tool settings"""
    pass


@click.command(short_help="Edit settings")
def edit():
    click.launch(str(DEFAULT_SETTINGS_PATH))
