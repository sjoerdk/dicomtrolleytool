from itertools import cycle
from unittest.mock import Mock

import pytest
from dicomtrolley.core import Query
from dicomtrolley.exceptions import DICOMTrolleyError
from dicomtrolley.trolley import Trolley

from dicomtrolleytool.query import (
    QueryErrorResult,
    QueryStudyResult,
    collect_query_results,
)


def test_query_result(an_image_level_study):
    """Query results should know whether they failed"""
    assert not QueryStudyResult(an_image_level_study[0], query=Query()).is_error()
    assert QueryErrorResult(DICOMTrolleyError("bad"), query=Query()).is_error()


@pytest.fixture
def a_trolley_with_errors(an_image_level_study):
    """A trolley that will return a study the first call and an exception the
    second call
    """
    a_trolley = Mock(spec_set=Trolley)
    a_trolley.find_study = Mock(
        side_effect=cycle([an_image_level_study[0], DICOMTrolleyError("BAD!")])
    )
    return a_trolley


def test_collect_query_results(a_trolley_with_errors):
    """Collect query results should complete despite errors"""
    results = collect_query_results(
        a_trolley_with_errors, [Query(AccessionNumber="1"), Query(AccessionNumber="2")]
    )
    assert not results[0].is_error()
    assert results[1].is_error()
