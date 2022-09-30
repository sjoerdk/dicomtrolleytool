from dicomtrolleytool.persistence import DiskSettings, TrolleyToolSettings


def test_settings(tmp_path):
    settings = TrolleyToolSettings(
        searcher_name="searcher", downloader_name="downloader"
    )

    settings_path = tmp_path / "test_settings.json"
    settings.save(path=settings_path)

    loaded = TrolleyToolSettings.parse_file(settings_path)
    assert settings.json() == loaded.json()


def test_disk_settings(tmp_path):
    path = tmp_path / "test_settings.json"
    assert not path.exists()
    disk_settings = DiskSettings(path=path)
    settings = disk_settings.get_settings()
    assert path.exists()
    loaded = TrolleyToolSettings.parse_file(path)
    assert loaded.json() == settings.json()
