from unittest.mock import Mock

import pytest

from dicomtrolleytool.cli.query import query_accession_number, query_suid


def test_basic_query_suid(context_runner):
    """Just invoking root cli command should not crash"""
    result = context_runner.invoke(query_suid, args=["123"], catch_exceptions=False)
    assert result.exit_code == 0


@pytest.fixture
def context_runner_with_image(context_runner, an_image_level_study):
    """A click context runner where trolley.find_study() returns a dicomtrolley Study
    at image level, with series and instance information
    """
    context_runner.mock_context.trolley.find_study = Mock(
        return_value=an_image_level_study[0]
    )
    return context_runner


def test_query_suid_include_fields(context_runner_with_image):
    """You can include custom fields to query, but they have to be valid DICOM tag
    names
    """
    result = context_runner_with_image.invoke(
        query_suid, args=["123", "--query-level", "Series"], catch_exceptions=False
    )

    assert result.exit_code == 0


def test_query_suid_multiple(context_runner_with_image):
    """You can pass multiple SUIDs to query_suid, as a comma or space separated
    list
    """
    result = context_runner_with_image.invoke(
        query_accession_number, args=["123, 323"], catch_exceptions=False
    )
    assert result.exit_code == 0


@pytest.mark.parametrize(
    "include_fields_value",
    ("InstanceCreatorUID,PatientID", "", "AccessionNumber"),  # empty is ok
)  # single value is ok
def test_query_include_fields(context_runner_with_image, include_fields_value):
    """You can add search fields to your search. These should work"""

    result = context_runner_with_image.invoke(
        query_accession_number,
        args=["123", "--include-fields", include_fields_value],
        catch_exceptions=False,
    )

    assert result.exit_code == 0


@pytest.mark.parametrize(
    "include_fields_value",
    (
        "not_a_keyword",
        "PatientID, AccesionNumber, not_a_keyword",
        "Modality,PatientName,",  # trailing comma not allowed
        "patientid",  # camelcase required
        "PATIENTID",
    ),
)
def test_query_include_fields_errors(context_runner_with_image, include_fields_value):
    """Some parameter checking should be done"""

    with pytest.raises(ValueError):
        context_runner_with_image.invoke(
            query_accession_number,
            args=["123", "--include-fields", include_fields_value],
            catch_exceptions=False,
        )
