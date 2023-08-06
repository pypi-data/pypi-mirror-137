from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Extra, conint, Field, validator

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class Pacticipant(BaseModel):
    name: str


class Matcher(BaseModel):
    match: Literal["equality", "regex", "type"]
    max: Optional[int]
    min: Optional[int]
    regex: Optional[str]


class MatchingBodyRule(BaseModel):
    matchers: List[Matcher]


class MatchingRule(BaseModel):
    body: Dict[str, MatchingBodyRule]


class ProviderState(BaseModel):
    name: str
    params: Optional[Dict]

    def full_name(self):
        if not self.params:
            return self.name
        return f"{self.name} {self._stringify_params()}"

    def _stringify_params(self):
        param_strings = [f"{k} {v}" for k, v in self.params.items()]
        return " ".join(param_strings)


class Headers(BaseModel):
    pass

    class Config:
        extra = Extra.allow


class Method(Enum):
    CONNECT = "CONNECT"
    DELETE = "DELETE"
    GET = "GET"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    POST = "POST"
    PUT = "PUT"
    TRACE = "TRACE"


class PactRequest(BaseModel):
    body: Optional[Any]
    headers: Optional[Headers]
    method: Method
    path: str
    query: Optional[Dict[str, List[str]]]

    @validator("method", pre=True)
    def validate_method(cls, v):
        return v.upper()


class PactResponse(BaseModel):
    body: Optional[Any]
    headers: Optional[Headers]
    matchingRules: Optional[MatchingRule]
    status: conint(ge=100, le=599)


class Interaction(BaseModel):
    description: str
    providerStates: Optional[List[ProviderState]]
    request: PactRequest
    response: PactResponse


class PactSpecification(BaseModel):
    version: str


class Metadata(BaseModel):
    pactSpecification: Optional[PactSpecification]


class Pact(BaseModel):
    consumer: Pacticipant
    interactions: List[Interaction]
    metadata: Optional[Metadata]
    provider: Pacticipant

    @property
    def version(self):
        if self.metadata is None or self.metadata.pactSpecification is None:
            return "2.0.0"
        return self.metadata.pactSpecification.version


# Input to template function


class RequestArgs(BaseModel):
    method: str
    path: str
    data: Optional[Dict]
    query_params: Optional[Dict]
    content_type: str = "application/json"


class TestMethodArgs(BaseModel):
    description: str = Field(
        ..., description="Unformatted name of test method to generate"
    )
    expectation: str = Field(
        ..., description="String representation of pact expectation dictionary"
    )
    request: RequestArgs


class TestCase(BaseModel):
    provider_state_names: List[str]
    test_methods: List[TestMethodArgs]

    @property
    def combined_provider_state_names(self) -> str:
        return " ".join(self.provider_state_names)

    @property
    def requires_provider_state(self) -> bool:
        return bool(self.provider_state_names)


class TestFile(BaseModel):
    pact_version: str
    base_class: str
    consumer: Pacticipant
    import_path: str
    provider: Pacticipant
    test_cases: List[TestCase]
