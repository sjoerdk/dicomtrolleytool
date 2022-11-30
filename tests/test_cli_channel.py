from dicomtrolleytool.cli.channel import cli_list
from dicomtrolleytool.cli.entrypoint import main
from tests.factories import TrolleyToolSettingsFactory


def test_cli_channel(context_runner):
    """Just invoking root cli command should not crash"""
    result = context_runner.invoke(
        main, args=["channel", "list"], catch_exceptions=False
    )
    assert result.exit_code == 0


def test_cli_channel_list(context_runner):
    """List should show a list of channels"""
    context_runner.mock_context.settings = TrolleyToolSettingsFactory(
        channels=["test_searcher", "test_downloader"]
    )
    result = context_runner.invoke(cli_list, catch_exceptions=False)
    assert "test_searcher" in result.output
