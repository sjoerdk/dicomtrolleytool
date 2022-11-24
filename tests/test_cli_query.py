from dicomtrolleytool.cli.query import suid


def test_cli_channel_list(context_runner):
    """Just invoking root cli command should not crash"""
    result = context_runner.invoke(suid, catch_exceptions=False)
    assert result.exit_code == 0
