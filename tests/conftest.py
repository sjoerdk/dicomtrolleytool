from click.testing import CliRunner


class MockContextCliRunner(CliRunner):
    """a click.testing.CliRunner that always passes a mocked context to any call"""

    def __init__(self, *args, mock_context, **kwargs):

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
