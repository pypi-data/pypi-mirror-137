from pactman.mock.pact import Pact as PactmanPact


def create_pactman_pact(
    consumer_name: str, provider_name: str, version: str
) -> PactmanPact:
    """
    Creates a real Pactman Pact given the consumer and provider names
    """
    # TODO: Do we need to set any of the additional fields?
    # host_name, port, pact_dir, use_mocking_server
    consumer = {"name": consumer_name}
    provider = {"name": provider_name}
    return PactmanPact(consumer, provider, version=version)
