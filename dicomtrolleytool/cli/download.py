"""Commands for downloading data"""
import tempfile

import click
from dicomtrolley.core import Query
from dicomtrolley.trolley import Trolley

from dicomtrolleytool.cli.base import TrolleyToolContext


@click.group()
@click.pass_obj
def download(context):
    """Download DICOM data"""


@click.command(short_help="Download by StudyInstanceUID")
@click.pass_obj
@click.argument("suid", type=str)
def download_suid(context: TrolleyToolContext, suid):
    """Query StudyInstanceUID"""
    trolley: Trolley = context.trolley
    study = trolley.find_study(Query(StudyInstanceUID=suid))
    download_dir = tempfile.gettempdir()
    trolley.download(study, output_dir=download_dir)


download.add_command(download_suid)
