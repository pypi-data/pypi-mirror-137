from pact_testgen.generator import generate_tests
from pact_testgen.dialects.django import Dialect


def test_django_test_generator_output_is_parsable(testfile):
    test_file, _ = generate_tests(testfile, Dialect())
    compile(test_file, "<string>", "exec")


def test_output_includes_expected_test_cases(testfile):
    test_file, _ = generate_tests(testfile, Dialect())
    # Names of test cases we expect to see. This is driven directly
    # by test_app/client_tests.py
    print(f"\nTEST FILE\n------\n\n{test_file}\n")
    assert "TestAnAuthorId1" in test_file
    assert "TestAnAuthorId1ABookExistsWithAuthorId1" in test_file
    assert "TestNoInitialState" in test_file
    assert "test_an_author_creation_request" in test_file
    assert "test_a_book_search_request_for_a_non_existent_author" in test_file
    assert "test_a_request_for_author_id_1" in test_file
    assert "test_an_author_update_request" in test_file
    assert "test_an_author_deletion_request" in test_file
    assert "test_a_book_search_request_for_author_id_1" in test_file


def test_provider_state_file_has_expected_methods(testfile):
    _, provider_state_file = generate_tests(testfile, Dialect())
    print(f"\nPROVIDER STATE FILE\n-------------------\n\n{provider_state_file}\n")
    assert "setup_nothing" not in provider_state_file
    assert "setup_an_author_id_1" in provider_state_file
    assert "setup_an_author_id_1_a_book_exists_with_author_id_1" in provider_state_file
