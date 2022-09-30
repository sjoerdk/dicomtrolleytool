"""Models ways of communicating with a DICOM server"""
from typing import Any, Dict, List

from dicomtrolleytool.exceptions import TrolleyToolError
from pydantic.main import BaseModel
from pydantic.types import SecretStr

from dicomtrolley.auth import create_session
from dicomtrolley.mint import Mint
from dicomtrolley.rad69 import Rad69


class Channel(BaseModel):
    """A ready-to-use channel of interaction with a DICOM server, with credentials"""

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
        return [name for name, f in self.__fields__.items() if f.type_ == SecretStr]


class MintChannel(Channel):
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


class Rad69Channel(Channel):
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


CHANNEL_CLASSES: Dict[str, Any] = {"rad69": Rad69Channel, "mint": MintChannel}


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