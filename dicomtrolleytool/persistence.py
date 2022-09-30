"""Functions and classes for handling settings and sensitive data."""
import pathlib
from io import StringIO
from typing import Optional

import keyring
from dicomtrolleytool.exceptions import DICOMTrolleyToolError
from pydantic.main import BaseModel


DEFAULT_SETTINGS_PATH = pathlib.Path.home() / "DICOMTrolleyToolSettings.yml"


class DICOMTrolleyToolSettings(BaseModel):

    searcher_name: str
    downloader_name: str

    query_missing: Optional[bool]

    # specific to rad69 downloader
    http_chunk_size: Optional[int]
    request_per_series: bool = True

    def write_to(self, stream: StringIO):
        """Persist this object to given stream"""
        stream.write(self.json())

    def save(self, path=None):
        if not path:
            path = DEFAULT_SETTINGS_PATH
        with open(path, "w") as f:
            self.write_to(f)


class Storage:
    """Something you can store data in."""

    def write(self, key, value):
        raise NotImplementedError()

    def read(self, key):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()


class KeyRingStorage(Storage):
    service_name = "dicomtrolleytool"

    def write(self, key, value):
        keyring.set_password(self.service_name, key, value)

    def read(self, key):
        return keyring.get_password(self.service_name, key)

    def delete(self, key):
        return keyring.delete_password(self.service_name, key)


class MemoryStorage(Storage):
    """Stores in memory. Only useful for testing."""

    def __init__(self):
        self.storage = {}

    def write(self, key, value):
        self.storage[key] = value

    def read(self, key):
        return self.storage.get(key)

    def delete(self, key):
        self.storage.pop([key])


class PersistenceError(DICOMTrolleyToolError):
    pass
