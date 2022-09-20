"""Functions and classes for handling the storage of sensitive data"""
import keyring


class Storage:
    """Something you can store data in"""

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
