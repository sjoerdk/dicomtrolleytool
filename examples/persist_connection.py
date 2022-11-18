from pydantic.types import SecretStr

from dicomtrolleytool.channels import DICOMQRChannel, MintChannel, Rad69Channel
from dicomtrolleytool.persistence import KeyRingStorage


storage = KeyRingStorage()

storage.save_channel(
    key="MintConnection1",
    channel=MintChannel(
        login_url="login_url",
        mint_url="mint_url",
        user="user",
        password=SecretStr("specialpass"),
        realm="realm",
    ),
)

storage.save_channel(
    key="Rad69Connection1",
    channel=Rad69Channel(
        login_url="login_url",
        rad69_url="rad69_url",
        user="user",
        password=SecretStr("specialpass"),
        realm="realm",
    ),
)

storage.save_channel(
    key="DICOMQRConnection",
    channel=DICOMQRChannel(
        host="hostname", port="1234", aet=SecretStr("target"), aec=SecretStr("calling")
    ),
)


print("Wrote connections to storage")
