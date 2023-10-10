from unittest.mock import Mock

from dicomtrolleytool.cli.query import query_suid


def test_basic_query_suid(context_runner):
    """Just invoking root cli command should not crash"""
    result = context_runner.invoke(query_suid, args=["123"], catch_exceptions=False)
    assert result.exit_code == 0


def test_query_suid_include_fields(context_runner, an_image_level_study):
    """You can include custom fields to query, but they have to be valid DICOM tag
    names
    """
    context_runner.mock_context.trolley.find_study = Mock(
        return_value=an_image_level_study[0]
    )  # return single study
    result = context_runner.invoke(
        query_suid, args=["123", "--query-level", "Series"], catch_exceptions=False
    )

    assert result.exit_code == 0
