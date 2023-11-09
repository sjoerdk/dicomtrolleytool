from pydantic.types import SecretStr

from dicomtrolleytool.channels import (
    DICOMQRChannel,
    DICOMWebChannel,
    MintChannel,
    Rad69Channel,
)
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

storage.save_channel(
    key="DICOM_WEB",
    channel=DICOMWebChannel(
        key="DICOM_WEB",
        description="A connection to host using DICOM-web",
        dicom_web_url="https://host/dicomweb",
        password=SecretStr("secret"),
        user="username",
    ),
)

print("Wrote connections to storage")
