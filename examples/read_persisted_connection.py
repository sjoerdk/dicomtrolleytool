from dicomtrolleytool.connections import MintConnection, Rad69Connection
from dicomtrolleytool.persistence import KeyRingStorage

storage = KeyRingStorage()
searcher = MintConnection.init_from_storage(storage, "MintConnection1")
downloader = Rad69Connection.init_from_storage(storage, "Rad69Connection1")

print(f"read connection from storage: {searcher}")
