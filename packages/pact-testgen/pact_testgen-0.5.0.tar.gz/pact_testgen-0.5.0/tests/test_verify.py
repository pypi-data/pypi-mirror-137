"""
Test the ``verify_reponse`` function.

We're not aiming for 100% coverage of matching rules here, since
we're relying on pactman for verification. These tests are
a sanity check that we're calling into pactman correctly.
"""
import json
from functools import partial
from typing import Any, Dict, List, Optional, Union

import pytest

from pact_testgen.public import Response, verify_response


@pytest.fixture
def verifier():
    return partial(verify_response, consumer_name="Consumer", provider_name="Provider")


def create_json_response(
    data: Union[Dict, List] = None, status_code=200, headers=Optional[Dict[str, Any]]
) -> Response:
    headers = headers or {"Content-Type": "application/json"}
    text = json.dumps(data) if data else ""
    return Response(text=text, status_code=status_code, headers=headers)


def test_verify_response_code_success(verifier):
    resp = create_json_response()

    result = verifier(pact_response={"status": 200}, actual_response=resp)

    result.assert_success()
    assert bool(result) is True


def test_verify_response_code_fail(verifier):
    resp = create_json_response()

    result = verifier(pact_response={"status": 201}, actual_response=resp)

    with pytest.raises(AssertionError) as error:
        result.assert_success()

    assert result.errors == ["Response status code 200 is not expected 201"]
    assert (
        str(error.value)
        == "Unexpected response: Response status code 200 is not expected 201"
    )
    assert bool(result) is False


def test_verify_type_success(verifier):
    # Values won't match, but types do
    resp = create_json_response({"id": 2, "name": "test"})
    expected_resp = {
        "body": {"id": 1, "name": "something"},
        "headers": None,
        "matchingRules": {
            "body": {
                "$": {
                    "matchers": [
                        {"match": "type", "max": None, "min": None, "regex": None}
                    ]
                }
            }
        },
        "status": 200,
    }

    result = verifier(pact_response=expected_resp, actual_response=resp)

    result.assert_success()
    assert bool(result) is True


def test_verify_type_fail(verifier):
    # Types won't match
    resp = create_json_response({"id": "not an integer", "name": "test"})
    expected_resp = {
        "body": {"id": 1, "name": "something"},
        "headers": None,
        "matchingRules": {
            "body": {
                "$": {
                    "matchers": [
                        {"match": "type", "max": None, "min": None, "regex": None}
                    ]
                }
            }
        },
        "status": 200,
    }

    result = verifier(pact_response=expected_resp, actual_response=resp)

    with pytest.raises(AssertionError) as error:
        result.assert_success()
    assert result.errors == [
        "body.id not correct type (string is not number) at body.id"
    ]

    assert str(error.value) == (
        "Unexpected response: body.id not correct type "
        "(string is not number) at body.id"
    )

    assert bool(result) is False
