from dicomtrolleytool.persistence import DICOMTrolleyToolSettings


def test_settings(tmp_path):
    settings = DICOMTrolleyToolSettings(
        searcher_name="searcher", downloader_name="downloader"
    )

    settings_path = tmp_path / "test_settings.json"
    settings.save(path=settings_path)

    loaded = DICOMTrolleyToolSettings.parse_file(settings_path)
    assert settings.json() == loaded.json()
