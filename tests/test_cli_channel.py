from pathlib import Path

from dicomtrolleytool.cli.channel import cli_list, set_searcher
from dicomtrolleytool.cli.entrypoint import main
from dicomtrolleytool.persistence import SettingsFile
from tests.factories import SettingsFromFileFactory, TrolleyToolSettingsFactory


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


def test_cli_set_searcher_list(context_runner, tmp_path):
    """Setting searcher should persist to settings file"""
    settings_path = Path(tmp_path) / "temp_settings.yml"
    context_runner.mock_context.settings = SettingsFromFileFactory(
        path=settings_path, channels=["searcher1", "downloader", "searcher2"]
    )

    assert SettingsFile(settings_path).load_settings().searcher_name == "VNA_MINT"
    result = context_runner.invoke(
        set_searcher, args=["searcher2"], catch_exceptions=False
    )
    assert result.exit_code == 0
    assert SettingsFile(settings_path).load_settings().searcher_name == "searcher2"
