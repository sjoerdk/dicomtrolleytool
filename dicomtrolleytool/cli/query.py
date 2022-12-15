"""For executing queries from command line"""
from typing import List

import click
from dicomtrolley.core import Query, Study
from dicomtrolley.trolley import Trolley

from dicomtrolleytool.cli.base import TrolleyToolContext, logger


@click.group()
def query():
    """Query DICOM data"""


@click.command(short_help="Query by StudyInstanceUID", name="suid")
@click.pass_obj
@click.argument("suid", type=str)
def query_suid(context: TrolleyToolContext, suid):
    """Query StudyInstanceUID"""
    trolley: Trolley = context.trolley
    result = trolley.find_study(
        Query(
            StudyInstanceUID=suid,
            include_fields=[
                "PatientID",
                "PatientBirthDate",
                "StudyDate",
                "ModalitiesInStudy",
            ],
        )
    )
    logger.info(result.data)


@click.command(short_help="Query by Accession Number", name="acc")
@click.pass_obj
@click.argument("acc_num", type=str)
def query_accession_number(context: TrolleyToolContext, acc_num):
    """Query StudyInstanceUID"""
    trolley: Trolley = context.trolley
    result = trolley.find_study(
        Query(
            AccessionNumber=acc_num,
            include_fields=[
                "StudyInstanceUID",
                "PatientID",
                "PatientBirthDate",
                "StudyDate",
                "ModalitiesInStudy",
            ],
        )
    )
    logger.info(result.data)


@click.command(short_help="Query by PatientID", name="patient_id")
@click.pass_obj
@click.argument("patient_id", type=str)
def query_patient_id(context: TrolleyToolContext, patient_id):
    """Query StudyInstanceUID"""
    trolley: Trolley = context.trolley
    results = trolley.find_studies(
        Query(
            PatientID=patient_id,
            include_fields=[
                "AccessionNumber",
                "StudyInstanceUID",
                "StudyDate",
                "ModalitiesInStudy",
            ],
        )
    )
    if results:
        results.sort(key=lambda x: x.data["StudyDate"].value, reverse=True)
        logger.info(f'Found {len(results)} studies for Patient "{patient_id}"')
        print("\n")
        print_to_console(studies_to_string(results))
    else:
        logger.info(f'no results found for PatientID "{patient_id}"')


def print_to_console(string_in):
    """Print string to console. Separate from logging to make multi-line
    output more manageable
    """
    print(string_in)


def study_to_string(study: Study) -> str:
    return f"Study {study.uid}\n" + "\n".join(str(x) for x in study.data)


def studies_to_string(studies: List[Study]) -> str:
    return "\n\n".join(list(study_to_string(x) for x in studies))


query.add_command(query_suid)
query.add_command(query_accession_number)
query.add_command(query_patient_id)
