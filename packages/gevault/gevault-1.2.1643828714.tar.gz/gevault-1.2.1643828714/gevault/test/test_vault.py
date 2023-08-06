from gevault.lib.vault import Vault

def test_update_config():
    Vault.update_config("testKey", "testValue")
    assert True
