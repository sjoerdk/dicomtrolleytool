"""Write a connection into storage"""

from dicomtrolleytool.connections import MintConnection, Rad69Connection
from dicomtrolleytool.persistence import KeyRingStorage
from pydantic.types import SecretStr

storage = KeyRingStorage()

searcher = MintConnection(
    login_url="login_url",
    mint_url="mint_url",
    user="user",
    password=SecretStr("specialpass"),
    realm="realm",
).write_to_storage(storage, key="MintConnection1")

downloader = Rad69Connection(
    login_url="login_url",
    rad69_url="rad69_url",
    user="user",
    password=SecretStr("specialpass"),
    realm="realm",
).write_to_storage(storage, key="Rad69Connection1")


print("Wrote connections to storage")
