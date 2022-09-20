"""Write a connection into storage"""

from dicomtrolleytool.connections import MintConnection
from dicomtrolleytool.persistence import KeyRingStorage
from pydantic.types import SecretStr

searcher = MintConnection(
    login_url="login_url",
    mint_url="mint_url",
    user="user",
    password=SecretStr("specialpass"),
    realm="realm",
)

storage = KeyRingStorage()
searcher.write_to_storage(storage, "Connection1")

print("Wrote connection to storage")
