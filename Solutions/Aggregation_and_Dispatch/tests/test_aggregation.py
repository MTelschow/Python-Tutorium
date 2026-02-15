import functools
import traceback

import numpy as np
import pytest

from numpy.testing import assert_allclose, assert_array_equal
from pytest_nbgrader.autotests import TestClass
from pytest_nbgrader.cases import execute, format_result


class TestAccumulateIf(TestClass):
    test_two_lists = TestClass.test_assertion
    test_arbitrary_iterables = TestClass.test_assertion
    test_iterators = TestClass.test_assertion


class TestMultiplyIf(TestClass):
    """Test for the `multiply_if` function."""

    @pytest.fixture
    def test_execution(cls, submission, cases, verbosity) -> tuple:
        """Run student submission on test cases."""
        if isinstance(cases.inputs[0][0], str):
            cases.inputs = (
                (eval(f'lambda {cases.inputs[0][0]}'), *cases.inputs[0][1:]),
                *cases.inputs[1:]
            )
        try:
            result = execute(submission, cases)
        except Exception as e:
            if cases.raises:
                # forward the (expected) exception to be checked
                result = e
            else:
                result = pytest.ExitCode.INTERNAL_ERROR
                limit = (verbosity > 0) - 1
                exception = traceback.format_exc(limit=limit)
                pytest.fail(
                    format_result(cases.inputs, result, exception=exception),
                    pytrace=False,
                )
        return cases, result
    
    test_two_lists = TestClass.test_assertion
    test_arbitrary_iterables = TestClass.test_assertion
    test_iterators = TestClass.test_assertion

class TestAggregate(TestClass):
    """Test for the `multiply_if` function."""

    @pytest.fixture
    def test_execution(cls, submission, cases, verbosity) -> tuple:
        """Run student submission on test cases."""
        if isinstance(cases.inputs[0][0], str):
            cases.inputs = (
                (eval(f'lambda {cases.inputs[0][0]}'), *cases.inputs[0][1:]),
                *cases.inputs[1:]
            )
        try:
            result = execute(submission, cases)
        except Exception as e:
            if cases.raises:
                # forward the (expected) exception to be checked
                result = e
            else:
                result = pytest.ExitCode.INTERNAL_ERROR
                limit = (verbosity > 0) - 1
                exception = traceback.format_exc(limit=limit)
                pytest.fail(
                    format_result(cases.inputs, result, exception=exception),
                    pytrace=False,
                )
        return cases, result
    
    test_boolean_mask = TestClass.test_assertion
    test_lambda_function = TestClass.test_assertion
