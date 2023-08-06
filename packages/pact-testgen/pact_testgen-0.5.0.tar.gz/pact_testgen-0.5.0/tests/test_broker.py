import pytest
import requests_mock
from requests.exceptions import HTTPError

from pact_testgen.broker import (
    BrokerConfig,
    _build_contract_url,
    _make_broker_request,
    get_pact_from_broker,
)
from pact_testgen.models import Metadata, Pact, PactSpecification, Pacticipant

from .utils import patch_env

BROKER_BASE_URL = "http://example.com"
PROVIDER = "TestProvider"
CONSUMER = "TestConsumer"
DEFAULT_URL = f"{BROKER_BASE_URL}/pacts/provider/{PROVIDER}/consumer/{CONSUMER}/latest"


@pytest.fixture
def brokerconfig():
    with patch_env():
        yield BrokerConfig(base_url=BROKER_BASE_URL)


def test_build_broker_url_default_version():
    url = _build_contract_url(
        BROKER_BASE_URL, provider_name=PROVIDER, consumer_name=CONSUMER
    )
    assert url == DEFAULT_URL


def test_build_broker_url_formatting_escapes():
    url = _build_contract_url(
        BROKER_BASE_URL,
        provider_name="Test Provider",
        consumer_name="Test Consumer",
    )
    assert url == (
        f"{BROKER_BASE_URL}/pacts/provider/Test%20Provider"
        "/consumer/Test%20Consumer/latest"
    )


def test_build_broker_url_with_consumer_version():
    VERSION = "123"
    url = _build_contract_url(
        BROKER_BASE_URL, provider_name=PROVIDER, consumer_name=CONSUMER, version=VERSION
    )
    assert url == (
        f"{BROKER_BASE_URL}/pacts/provider/{PROVIDER}"
        f"/consumer/{CONSUMER}/version/{VERSION}"
    )


def test_broker_request_throws(brokerconfig):
    with requests_mock.Mocker() as m:
        m.get(DEFAULT_URL, status_code=404, reason="Not Found")

        with pytest.raises(HTTPError):
            _make_broker_request(DEFAULT_URL)


def test_receive_expected_response(brokerconfig):
    pact = Pact(
        consumer=Pacticipant(name=CONSUMER),
        provider=Pacticipant(name=PROVIDER),
        metadata=Metadata(PactSpecification=PactSpecification(version="3.0.0")),
        interactions=[],
    )

    with requests_mock.Mocker() as m:
        m.get(DEFAULT_URL, text=pact.json())

        retrieved_pact = get_pact_from_broker(
            broker_config=brokerconfig, provider_name=PROVIDER, consumer_name=CONSUMER
        )

        assert retrieved_pact == pact
