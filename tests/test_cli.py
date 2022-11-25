from dicomtrolleytool.cli.entrypoint import main
from dicomtrolleytool.cli.base import status


def test_cli_base(context_runner):
    """Just invoking root cli command should not crash"""
    assert context_runner.invoke(main).exit_code == 0


def test_cli_status(context_runner):
    """Just invoking root cli command should not crash"""
    result = context_runner.invoke(status, catch_exceptions=False)
    assert "Settings file" in result.output
