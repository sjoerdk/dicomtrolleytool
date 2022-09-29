"""Models things that can directly connect to a DICOM server"""
import json
from typing import List

from dicomtrolleytool.persistence import Storage
from pydantic.main import BaseModel
from pydantic.types import SecretStr

from dicomtrolley.auth import create_session
from dicomtrolley.mint import Mint
from dicomtrolley.rad69 import Rad69


class Connection(BaseModel):
    @classmethod
    def init_from_storage(cls, storage: Storage, key: str):
        """Init the connection stored under key"""
        params = json.loads(storage.read(key))
        return cls(**params)

    def write_to_storage(self, storage: Storage, key: str):
        """Write this connection to storage under key"""
        params = self.dict()
        for name in self.get_secret_param_names():  # avoid writing '******'
            params[name] = getattr(self, name).get_secret_value()
        storage.write(key, json.dumps(params))

    def get_secret_param_names(self) -> List[str]:
        return [name for name, f in self.__fields__.items() if f.type_ == SecretStr]


class MintConnection(Connection):
    """Can do DICOM searches with MINT

    Wrapper around dicomtrolley Mint.
    """

    login_url: str
    mint_url: str
    user: str
    password: SecretStr
    realm: str

    def init_searcher(self) -> Mint:
        """Create a downloader instance from this connection"""
        session = create_session(
            self.login_url, self.user, self.password.get_secret_value(), self.realm
        )
        return Mint(session, self.mint_url)


class Rad69Connection(Connection):
    """Can do DICOM downloads with the rad69 protocol"""

    login_url: str
    rad69_url: str
    user: str
    password: SecretStr
    realm: str

    def init_downloader(self) -> Rad69:
        """Create a searcher instance from this connection"""
        session = create_session(
            self.login_url, self.user, self.password.get_secret_value(), self.realm
        )
        return Rad69(session=session, url=self.rad69_url)
