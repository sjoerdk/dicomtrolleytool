import factory

from dicomtrolleytool.persistence import TrolleyToolSettings


class TrolleyToolSettingsFactory(factory.Factory):
    class Meta:
        model = TrolleyToolSettings

    searcher_name = "a_searcher"
    downloader_name = "a_downloader"

    channels = factory.List(
        ["a_searcher", "a_downloader", factory.Sequence(lambda n: f"other_channel_{n}")]
    )
