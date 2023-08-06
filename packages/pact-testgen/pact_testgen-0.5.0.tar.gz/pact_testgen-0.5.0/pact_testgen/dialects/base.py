from abc import ABC, abstractmethod, abstractproperty

import black

from pact_testgen.models import TestCase


class BaseDialect(ABC):
    @abstractmethod
    def get_setup_function_name(self, test_case: TestCase):
        ...

    @abstractproperty
    def method_template(self):
        ...

    @abstractproperty
    def test_case_template(self):
        ...

    @abstractproperty
    def test_file_template(self):
        ...

    @abstractproperty
    def provider_state_template(self):
        ...


class PythonFormatter:
    def __init__(self, line_length=88):
        self.line_length = line_length

    def format(self, content: str) -> str:
        mode = black.Mode(line_length=self.line_length)
        return black.format_str(content, mode=mode)
