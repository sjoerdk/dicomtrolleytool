import pytest as pytest
from dicomtrolleytool.channels import MintChannel
from dicomtrolleytool.persistence import MemoryStorage


@pytest.fixture
def a_mint_connection():
    return MintChannel(
        key="test_channel",
        login_url="login_url",
        mint_url="mint_url",
        user="user",
        password="specialpass",
        realm="realm",
    )


def test_write_to_storage(a_mint_connection):

    storage = MemoryStorage()
    storage.save_channel("test", a_mint_connection)
    loaded = storage.load_channel("test")
    assert (
        loaded.password.get_secret_value()
        == a_mint_connection.password.get_secret_value()
    )
    assert loaded.json() == a_mint_connection.json()
