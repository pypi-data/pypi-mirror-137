from typing import Tuple

from .dialects.base import BaseDialect as Dialect
from .models import TestFile


def generate_tests(test_file: TestFile, dialect: Dialect) -> Tuple[str, str]:
    cases = []
    provider_state_setup_functions = []
    consumer_name = test_file.consumer.name
    provider_name = test_file.provider.name

    for test_case in test_file.test_cases:

        methods = dialect.method_template.render(
            test_case=test_case,
            consumer_name=consumer_name,
            provider_name=provider_name,
            pact_version=test_file.pact_version,
        )

        assert methods, "Failed to generate test methods"

        if test_case.requires_provider_state:
            setup_function_name = dialect.get_setup_function_name(test_case)
        else:
            setup_function_name = None

        case = dialect.test_case_template.render(
            ps_names=test_case.combined_provider_state_names,
            file=test_file,
            methods=methods,
            setup_function_name=setup_function_name,
        )
        cases.append(case)
        if test_case.requires_provider_state:
            provider_state_setup_functions.append(
                {
                    "method_name": setup_function_name,
                    "provider_states": test_case.provider_state_names,
                }
            )

    all_tests = dialect.test_file_template.render(
        file=test_file, cases=cases, setup_functions=provider_state_setup_functions
    )

    provider_states = dialect.provider_state_template.render(
        setup_functions=provider_state_setup_functions
    )
    return all_tests, provider_states
