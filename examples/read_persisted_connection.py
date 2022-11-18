from dicomtrolleytool.persistence import KeyRingStorage

storage = KeyRingStorage()
searcher = storage.load_channel("MintConnection1").init_searcher()
downloader = storage.load_channel("Rad69Connection1").init_downloader()

print(f"read connection from storage: {searcher}")
