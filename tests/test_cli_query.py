from dicomtrolleytool.cli.query import query_suid


def test_cli_channel_list(context_runner):
    """Just invoking root cli command should not crash"""
    result = context_runner.invoke(query_suid, args=["123"], catch_exceptions=False)
    assert result.exit_code == 0
