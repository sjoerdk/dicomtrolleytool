"""Functions and classes for handling settings and sensitive data."""
import json
import pathlib
from io import StringIO
from typing import Optional

import keyring
from pydantic.main import BaseModel

from .channels import Channel, ChannelFactory
from .exceptions import TrolleyToolError
from .logging import get_module_logger

logger = get_module_logger("persistence")

DEFAULT_SETTINGS_PATH = (
    pathlib.Path.home() / ".trolleytool" / "DICOMTrolleyToolSettings.yml"
)


class TrolleyToolSettings(BaseModel):

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


class DiskSettings:
    def __init__(self, path=None):
        if not path:
            path = DEFAULT_SETTINGS_PATH
        self.path = path

    def get_settings(self):
        self.assert_settings()
        return TrolleyToolSettings.parse_file(self.path)

    def assert_settings(self):
        if not self.path.exists():
            logger.info(
                f"No settings file found. Creating default settings at "
                f'"{self.path}"'
            )
            parent = self.path.parent
            if not parent.exists():
                parent.mkdir(parents=True)
            with open(self.path, "w") as f:
                self.get_default_settings().write_to(f)

    @staticmethod
    def get_default_settings():
        return TrolleyToolSettings(
            searcher_name="VNA_MINT", downloader_name="VNA_RAD69"
        )


class Storage:
    """Something you can store channels in.

    Will persist channel class with an extra key
    """

    class_key_param = "class_key"  # save class in this

    def save_value(self, key, value):
        raise NotImplementedError()

    def load_value(self, key):
        raise NotImplementedError()

    def delete(self, key):
        raise NotImplementedError()

    def save_channel(self, key, channel: Channel):
        """Saves chanel parameters and adds type as a parameter"""
        as_dict = channel.to_dict()
        if as_dict.get(self.class_key_param):
            raise TrolleyToolError(f'Key "{self.class_key_param}" is already taken')
        as_dict[self.class_key_param] = ChannelFactory.get_class_key(channel)
        self.save_value(key, json.dumps(as_dict))

    def load_channel(self, key):
        loaded = json.loads(self.load_value(key))
        class_key = loaded.pop(self.class_key_param)
        return ChannelFactory.get_chanel_class(class_key).init_from_dict(loaded)


class KeyRingStorage(Storage):
    service_name = "dicomtrolleytool"

    def save_value(self, key, value):
        keyring.set_password(self.service_name, key, value)

    def load_value(self, key):
        return keyring.get_password(self.service_name, key)

    def delete(self, key):
        return keyring.delete_password(self.service_name, key)


class MemoryStorage(Storage):
    """Stores in memory. Only useful for testing."""

    def __init__(self):
        self.storage = {}

    def save_value(self, key, value):
        self.storage[key] = value

    def load_value(self, key):
        return self.storage.get(key)

    def delete(self, key):
        self.storage.pop([key])


class PersistenceError(TrolleyToolError):
    pass
