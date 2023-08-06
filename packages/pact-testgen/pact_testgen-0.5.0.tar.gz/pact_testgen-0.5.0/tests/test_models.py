from pact_testgen.models import ProviderState


def test_provider_state_full_name():
    ps = ProviderState(name="A thing exists")
    assert ps.full_name() == "A thing exists"

    ps = ProviderState(name="A thing exists", params={"id": 1})
    assert ps.full_name() == "A thing exists id 1"
