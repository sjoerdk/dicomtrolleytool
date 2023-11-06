import pytest
from dicomtrolley.core import Query
from dicomtrolley.exceptions import DICOMTrolleyError

from dicomtrolleytool.cli.output import (
    FormatLevel,
    ResultFormat,
    format_query_results,
    format_query_results_table,
)
from dicomtrolleytool.query import QueryErrorResult


@pytest.fixture
def some_query_results_with_error(some_query_results):
    """Some successful image level query results and one error"""
    return some_query_results + [
        QueryErrorResult(
            content=DICOMTrolleyError("Something went wrong"),
            query=Query(AccessionNumber="4"),
        )
    ]


def test_format_query_results_raw(some_query_results_with_error):
    text = format_query_results(
        some_query_results_with_error, output_format=ResultFormat.RAW
    )
    assert some_query_results_with_error[0].content.uid in text
    assert some_query_results_with_error[0].content.series[0].uid in text
    assert some_query_results_with_error[0].content.series[0].instances[0].uid in text
    # just some basic checks for content. Format looks fine visually


def test_format_query_results_table(some_query_results_with_error):

    table_text = format_query_results_table(
        some_query_results_with_error, format_level=FormatLevel.STUDY
    )

    assert table_text
