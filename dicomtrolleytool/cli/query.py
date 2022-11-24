"""For executing queries from command line"""

import click
from dicomtrolley.core import Query
from dicomtrolley.trolley import Trolley

from dicomtrolleytool.cli.cli_core import TrolleyToolContext


@click.group()
@click.pass_obj
def query(context):
    """Query DICOM data"""


@click.command(short_help="Query by StudyInstanceUID")
@click.pass_obj
@click.argument("suid", type=str)
def suid(context: TrolleyToolContext, suid):
    """Query StudyInstanceUID"""
    trolley: Trolley = context.trolley
    result = trolley.find_study(Query(StudyInstanceUID=suid))
    print(result)


query.add_command(suid)
