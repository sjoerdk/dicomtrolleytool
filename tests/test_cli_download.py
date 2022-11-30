from dicomtrolleytool.cli.download import download_suid


def test_cli_download(context_runner):
    """Just invoking root cli command should not crash"""
    result = context_runner.invoke(download_suid, args=["123"], catch_exceptions=False)
    assert result.exit_code == 0
