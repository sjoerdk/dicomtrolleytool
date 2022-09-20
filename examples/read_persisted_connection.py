from dicomtrolleytool.connections import MintConnection
from dicomtrolleytool.persistence import KeyRingStorage

storage = KeyRingStorage()
searcher = MintConnection.init_from_storage(storage, "Connection1")

print(f"read connection from storage: {searcher}")
