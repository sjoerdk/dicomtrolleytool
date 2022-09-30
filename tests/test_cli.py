from unittest.mock import Mock

import pytest as pytest
from dicomtrolleytool.cli.entrypoint import TrolleyToolContext, main, status

from dicomtrolley.trolley import Trolley
from tests.conftest import MockContextCliRunner


@pytest.fixture
def context_runner():
    """Click test runner that injects mock context"""
    return MockContextCliRunner(
        mock_context=TrolleyToolContext(trolley=Mock(spec_set=Trolley))
    )


def test_cli_base(context_runner):
    """Just invoking root cli command should not crash"""
    assert context_runner.invoke(main).exit_code == 0


def test_cli_status(context_runner):
    """Just invoking root cli command should not crash"""
    result = context_runner.invoke(status, catch_exceptions=False)
    assert "Settings file" in result.output
