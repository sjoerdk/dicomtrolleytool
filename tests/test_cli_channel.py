from dicomtrolleytool.cli.channel import cli_list
from tests.factories import TrolleyToolSettingsFactory


def test_cli_channel_list(context_runner):
    """Just invoking root cli command should not crash"""
    context_runner.mock_context.settings = TrolleyToolSettingsFactory()
    result = context_runner.invoke(cli_list, catch_exceptions=False)
    assert "a_searcher" in result.output
