"""For executing queries from command line"""
from typing import List

import click
from click import Choice
from dicomtrolley.core import Query, QueryLevels, Study
from dicomtrolley.trolley import Trolley

from dicomtrolleytool.cli.base import TrolleyToolContext, logger


@click.group()
def query():
    """Query DICOM data"""


# Ask for these fields if not specified
DEFAULT_INCLUDE_FIELDS_STUDY = [
    "PatientID",
    "PatientBirthDate",
    "StudyDate",
    "ModalitiesInStudy",
    "NumberOfStudyRelatedInstances",
]

DEFAULT_INCLUDE_FIELDS_SERIES = [
    "SeriesInstanceUID",
    "SeriesDate",
    "SeriesDescription",
    "Modality",
    "ProtocolName",
]

DEFAULT_INCLUDE_FIELDS_INSTANCE = [
    "SOPClassUID",
    "Rows",
    "Columns",
    "StationName",
    "SoftwareVersions",
]


def get_default_include_fields(query_level):
    """DICOM fields to include for different levels of queries"""
    if query_level == QueryLevels.STUDY:
        return DEFAULT_INCLUDE_FIELDS_STUDY
    elif query_level == QueryLevels.SERIES:
        return DEFAULT_INCLUDE_FIELDS_STUDY + DEFAULT_INCLUDE_FIELDS_SERIES
    elif query_level == QueryLevels.INSTANCE:
        return (
            DEFAULT_INCLUDE_FIELDS_STUDY
            + DEFAULT_INCLUDE_FIELDS_SERIES
            + DEFAULT_INCLUDE_FIELDS_INSTANCE
        )


@click.command(short_help="Query by StudyInstanceUID", name="suid")
@click.pass_obj
@click.argument("suid", type=str)
@click.option(
    "--query-level",
    type=Choice(choices=[x.name for x in QueryLevels], case_sensitive=False),
    default=QueryLevels.STUDY,
    help="Show information on study, series or instance level",
    show_default=True,
)
def query_suid(context: TrolleyToolContext, suid, query_level):
    """Query StudyInstanceUID"""
    trolley: Trolley = context.trolley
    result = trolley.find_study(
        Query(
            StudyInstanceUID=suid,
            include_fields=get_default_include_fields(query_level),
            query_level=query_level,
        )
    )

    logger.info(result.data)
    if result.series:
        logger.info("All series")
        for x in result.series:
            logger.info(x.data)


@click.command(short_help="Query by Accession Number", name="acc")
@click.pass_obj
@click.argument("acc_num", type=str)
def query_accession_number(context: TrolleyToolContext, acc_num):
    """Query StudyInstanceUID"""
    trolley: Trolley = context.trolley
    result = trolley.find_study(
        Query(
            AccessionNumber=acc_num,
            include_fields=["StudyInstanceUID"] + DEFAULT_INCLUDE_FIELDS_STUDY,
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
