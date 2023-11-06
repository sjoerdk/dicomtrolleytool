from typing import List
from unittest.mock import Mock

import pytest
from click.testing import CliRunner
from dicomtrolley.core import Query
from dicomtrolley.dicom_qr import DICOMQR
from dicomtrolley.trolley import Trolley
from pydicom import Dataset
from pydicom.tag import Tag

from dicomtrolleytool.cli.base import TrolleyToolContext
from dicomtrolleytool.persistence import TrolleyToolSettings
from dicomtrolleytool.query import QueryStudyResult


@pytest.fixture
def some_channels():
    return {"channel1", "channel2", "channel3"}


@pytest.fixture
def context_runner(some_channels, a_study_level_study):
    """Click test runner that injects mock context"""
    a_trolley = Mock(spec_set=Trolley)
    a_trolley.find_study = Mock(
        return_value=a_study_level_study[0]
    )  # return single study
    return MockContextCliRunner(
        mock_context=TrolleyToolContext(
            settings=Mock(spec_set=TrolleyToolSettings), trolley=a_trolley
        )
    )


class MockContextCliRunner(CliRunner):
    """a click.testing.CliRunner that always passes a mocked context to any call"""

    def __init__(self, *args, mock_context: TrolleyToolContext, **kwargs):

        super().__init__(*args, **kwargs)
        self.mock_context = mock_context

    def invoke(
        self,
        cli,
        args=None,
        input=None,
        env=None,
        catch_exceptions=True,
        color=False,
        **extra,
    ):
        return super().invoke(
            cli,
            args,
            input,
            env,
            catch_exceptions,
            color,
            obj=self.mock_context,
        )


def quick_dataset(*_, **kwargs) -> Dataset:
    """Creates a pydicom dataset with keyword args as tagname - value pairs

    Examples
    --------
    >>> ds = quick_dataset(PatientName='Jane', StudyDescription='Test')
    >>> ds.PatientName
    'Jane'
    >>> ds.StudyDescription
    'Test'

    Raises
    ------
    ValueError
        If any input key is not a valid DICOM keyword

    """
    dataset = Dataset()
    dataset.is_little_endian = True  # required common meta header choice
    dataset.is_implicit_VR = False  # required common meta header choice
    for tag_name, value in kwargs.items():
        Tag(tag_name)  # assert valid dicom keyword. pydicom will not do this.
        dataset.__setattr__(tag_name, value)
    return dataset


def create_c_find_study_response(study_instance_uids) -> List[Dataset]:
    """Datasets like the ones returned from a successful STUDY level CFIND with
    PatientRootQueryRetrieveInformationModelFind
    """
    response = []
    for study_instance_uid in study_instance_uids:
        response.append(
            quick_dataset(StudyInstanceUID=study_instance_uid, Modality="CT")
        )

    return response


@pytest.fixture
def a_study_level_study():
    """Study witnout slice info"""
    return DICOMQR.parse_c_find_response(
        create_c_find_study_response(study_instance_uids=["Study2"])
    )


def create_c_find_image_response(
    study_instance_uid,
    series_instance_uids: List[str],
    sop_class_uids: List[str],
) -> List[Dataset]:
    """Datasets like the ones returned from a successful IMAGE level CFIND with
    PatientRootQueryRetrieveInformationModelFind
    Instances that each contain uids to their containing series and studies
    """
    responses = []
    for series_instance_uid in series_instance_uids:
        for sop_instance_uid in sop_class_uids:
            responses.append(
                quick_dataset(
                    StudyInstanceUID=study_instance_uid,
                    SeriesInstanceUID=series_instance_uid,
                    SOPInstanceUID=sop_instance_uid,
                )
            )
    return responses


@pytest.fixture
def an_image_level_study():
    """A study with series and slice info"""
    response = create_c_find_image_response(
        study_instance_uid="Study1",
        series_instance_uids=["Series1", "Series2"],
        sop_class_uids=[f"Instance{i}" for i in range(1, 10)],
    )
    return DICOMQR.parse_c_find_response(response)


@pytest.fixture()
def some_query_results(an_image_level_study):
    return [
        QueryStudyResult(an_image_level_study[0], Query(AccessionNumber="1")),
        QueryStudyResult(an_image_level_study[0], Query(AccessionNumber="2")),
        QueryStudyResult(an_image_level_study[0], Query(AccessionNumber="3")),
    ]
