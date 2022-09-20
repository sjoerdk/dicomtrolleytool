from dicomtrolleytool.connections import MintConnection
from dicomtrolleytool.persistence import MemoryStorage


def test_write_to_storage():
    searcher = MintConnection(login_url='login_url',
                              mint_url='mint_url',
                              user='user',
                              password='specialpass',
                              realm='realm')

    storage = MemoryStorage()
    searcher.write_to_storage(storage, 'test')
    loaded = MintConnection.init_from_storage(storage, 'test')
    assert loaded.password.get_secret_value() == searcher.password.get_secret_value()
    assert loaded.json() == searcher.json()


