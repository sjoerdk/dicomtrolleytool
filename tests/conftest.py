from unittest.mock import Mock

import pytest
from click.testing import CliRunner
from dicomtrolley.trolley import Trolley

from dicomtrolleytool.cli.cli_core import TrolleyToolContext
from dicomtrolleytool.persistence import TrolleyToolSettings


@pytest.fixture
def some_channels():
    return {"channel1", "channel2", "channel3"}


@pytest.fixture
def context_runner(some_channels):
    """Click test runner that injects mock context"""
    return MockContextCliRunner(
        mock_context=TrolleyToolContext(
            settings=Mock(spec_set=TrolleyToolSettings), trolley=Mock(spec_set=Trolley)
        )
    )


class MockContextCliRunner(CliRunner):
    """a click.testing.CliRunner that always passes a mocked context to any call"""

    def __init__(self, *args, mock_context: TrolleyToolContext, **kwargs):

        super().__init__(*args, **kwargs)
        self.mock_context = mock_context

    def invoke(
        self,
        cli,
        args=None,
        input=None,
        env=None,
        catch_exceptions=True,
        color=False,
        **extra
    ):
        return super().invoke(
            cli,
            args,
            input,
            env,
            catch_exceptions,
            color,
            obj=self.mock_context,
        )
