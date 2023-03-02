import tempfile
from pathlib import Path

import factory

from dicomtrolleytool.persistence import SettingsFromFile, TrolleyToolSettings


class TrolleyToolSettingsFactory(factory.Factory):
    class Meta:
        model = TrolleyToolSettings

    searcher_name = "a_searcher"
    downloader_name = "a_downloader"

    channels = factory.List(
        ["a_searcher", "a_downloader", factory.Sequence(lambda n: f"other_channel_{n}")]
    )


class SettingsFromFileFactory(factory.Factory):
    class Meta:
        model = SettingsFromFile

    path = Path(tempfile.gettempdir()) / "temp_settings.yml"
    searcher_name = "a_searcher"
    downloader_name = "a_downloader"

    channels = factory.List(
        ["a_searcher", "a_downloader", factory.Sequence(lambda n: f"other_channel_{n}")]
    )
