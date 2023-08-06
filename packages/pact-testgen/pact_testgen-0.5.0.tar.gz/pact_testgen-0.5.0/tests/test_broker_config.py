from pact_testgen.broker import BrokerBasicAuthConfig, BrokerConfig

from .utils import patch_env

AUTH = {
    "username": "broker-username",
    "password": "broker-password",
}
DEFAULTS = {
    "base_url": "http://example.com",
    "auth": AUTH,
}

# i.e. ENV_DEFAULTS = {"PACT_BROKER_BASE_URL": ...}
ENV_DEFAULTS = {
    "PACT_BROKER_BASE_URL": DEFAULTS["base_url"],
    "PACT_BROKER_USERNAME": AUTH["username"],
    "PACT_BROKER_PASSWORD": AUTH["password"],
}


@patch_env(ENV_DEFAULTS)
def test_set_from_env():
    config = BrokerConfig(auth=BrokerBasicAuthConfig())
    assert config.base_url == DEFAULTS["base_url"]
    assert config.auth.username == AUTH["username"]
    assert config.auth.password == AUTH["password"]


@patch_env(ENV_DEFAULTS)
def test_none_init_values_defaults_to_env():
    config = BrokerConfig(
        base_url=None, auth=BrokerBasicAuthConfig(username=None, password=None)
    )
    assert config.base_url == DEFAULTS["base_url"]
    assert config.auth.username == AUTH["username"]
    assert config.auth.password == AUTH["password"]


@patch_env(ENV_DEFAULTS)
def test_init_values_override_env():
    values = {
        "base_url": "http://example.com:8000",
        "auth": {
            "username": "new-username",
            "password": "new-password",
        },
    }
    config = BrokerConfig(**values)
    assert config.base_url == values["base_url"]
    assert config.auth.username == values["auth"]["username"]
    assert config.auth.password == values["auth"]["password"]


@patch_env()
def test_auth_tuple_no_creds():
    config = BrokerConfig(base_url="http://example.com")
    assert config.auth_tuple is None


@patch_env()
def test_auth_tuple_with_creds():
    config = BrokerConfig(**DEFAULTS)
    assert config.auth_tuple == (AUTH["username"], AUTH["password"])
