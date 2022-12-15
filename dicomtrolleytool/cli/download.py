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


@click.command(short_help="Download by StudyInstanceUID", name="suid")
@click.pass_obj
@click.option("-o", "--output-dir")
@click.argument("suid", type=str)
def download_suid(context: TrolleyToolContext, suid, output_dir):
    """Query StudyInstanceUID"""
    trolley: Trolley = context.trolley
    study = trolley.find_study(Query(StudyInstanceUID=suid))
    if output_dir is None:
        download_dir = tempfile.gettempdir()
    else:
        download_dir = output_dir
    trolley.download(study, output_dir=download_dir)


download.add_command(download_suid)
