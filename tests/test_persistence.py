import pytest

from dicomtrolleytool.persistence import (
    SettingsFile,
    KeyRingStorage,
    MemoryStorage,
    PersistenceError,
    SettingsFromFile,
)


def test_settings(tmp_path):
    settings_path = tmp_path / "test_settings.json"
    settings = SettingsFromFile(
        path=settings_path, searcher_name="searcher", downloader_name="downloader"
    )
    settings.save()

    loaded = SettingsFile(settings_path).load_settings()
    assert settings.json() == loaded.json()


def test_disk_settings(tmp_path):
    path = tmp_path / "test_settings.json"
    assert not path.exists()
    disk_settings = SettingsFile(path=path)
    disk_settings.load_settings()
    assert path.exists()  # loading non-existant should create


def test_channel_not_found():
    """Translate unhelpful loading error into something a user can use"""
    with pytest.raises(PersistenceError):
        KeyRingStorage().load_channel("UNKNOWN")

    with pytest.raises(PersistenceError):
        MemoryStorage().load_channel("NOT_THERE")
