"""Models ways of communicating with a DICOM server"""
from typing import Any, Dict, List

import requests
from dicomtrolley.core import Downloader, Searcher
from dicomtrolley.qido_rs import QidoRS
from dicomtrolley.wado_rs import WadoRS
from pydantic.main import BaseModel
from pydantic.types import SecretStr
from dicomtrolley.auth import create_session
from dicomtrolley.dicom_qr import DICOMQR
from dicomtrolley.mint import Mint
from dicomtrolley.rad69 import Rad69
from requests.auth import HTTPBasicAuth

from dicomtrolleytool.exceptions import TrolleyToolError
from dicomtrolleytool.logs import get_module_logger

logger = get_module_logger("channels")


class Channel(BaseModel):
    """A ready-to-use channel of interaction with a DICOM server, with credentials

    Can be persisted to disk
    """

    key: str  # for storage and retrieval
    description: str = ""  # single-line human-readable description

    @classmethod
    def init_from_dict(cls, dict_in):
        """Init the connection stored under key"""
        return cls(**dict_in)

    def to_dict(self):
        """Channel as dict. Includes plain text secrets"""
        params = self.dict()
        for name in self.get_secret_param_names():  # avoid writing '******'
            params[name] = getattr(self, name).get_secret_value()
        return params

    def get_secret_param_names(self) -> List[str]:
        return [
            name for name, f in self.model_fields.items() if f.annotation == SecretStr
        ]


class DownloaderChannel(Channel):
    def init_downloader(self) -> Downloader:
        raise NotImplementedError()


class SearcherChannel(Channel):
    def init_searcher(self) -> Searcher:
        raise NotImplementedError()


class MintChannel(SearcherChannel):
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


class Rad69Channel(DownloaderChannel):
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


class DICOMQRChannel(SearcherChannel):
    """Query using dicom QR"""

    host: str
    port: str
    aet: SecretStr
    aec: SecretStr

    def init_searcher(self) -> Mint:
        """Create a downloader instance from this connection"""

        return DICOMQR(
            host=self.host,
            port=int(self.port),
            aet=self.aet.get_secret_value(),
            aec=self.aec.get_secret_value(),
        )


class DICOMWebChannel(SearcherChannel):
    """QIDO-RS and WADO-RS. Optionally over the same connection"""

    dicom_web_url: str
    user: str
    password: SecretStr

    def get_session(self):
        session = requests.Session()
        logger.debug(f'Creating basic auth session with user "{self.user}"')
        session.auth = HTTPBasicAuth(
            username=self.user, password=self.password.get_secret_value()
        )
        return session

    def init_downloader(self, session=None) -> WadoRS:
        if not session:
            logger.debug("WadoRS session not given. Creating new one")
            session = self.get_session()
        return WadoRS(session=session, url=self.dicom_web_url)

    def init_searcher(self, session=None) -> QidoRS:
        if not session:
            logger.debug("QidoRS session not given. Creating new one")
            session = self.get_session()
        return QidoRS(session=session, url=self.dicom_web_url)


CHANNEL_CLASSES: Dict[str, Any] = {
    "rad69": Rad69Channel,
    "mint": MintChannel,
    "dicomqr": DICOMQRChannel,
    "dicomweb": DICOMWebChannel,
}


class ChannelFactory:
    """Maps channel classes to string names"""

    classes = CHANNEL_CLASSES
    class_keys = {cls: key for key, cls in CHANNEL_CLASSES.items()}

    @classmethod
    def get_class_key(cls, channel):
        """Get key corresponding to channel instance type"""
        try:
            return cls.class_keys[type(channel)]
        except KeyError as e:
            raise ChannelFactoryError(
                f"Key for channel type '{type(channel)}'. "
                f"Available: {list(cls.classes.values())}"
            ) from e

    @classmethod
    def get_chanel_class(cls, class_key):
        try:
            return cls.classes[class_key]
        except KeyError as e:
            raise ChannelFactoryError(
                f"Unknown class key '{class_key}'. "
                f"Available: {list(cls.classes.keys())}"
            ) from e


class ChannelFactoryError(TrolleyToolError):
    pass
