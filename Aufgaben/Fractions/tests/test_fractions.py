import math
import traceback
from enum import Enum

import numpy as np
import pytest
from pytest_nbgrader.cases import execute, format_result


def reduce(n, d):
    """reduce fraction and set d positive"""
    gcd, sign = math.gcd(n, d), -1 if (n < 0) ^ (d < 0) else +1
    return int(math.copysign(n, sign)) // gcd, abs(d) // gcd


class Execution:
    """Base class for generating instances with given cases."""

    @pytest.fixture
    def test_execution(cls, submission, cases, verbosity) -> list:
        """Run student submission on test cases."""

        try:
            result, *_ = execute(submission, cases)
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


class TestInstantiation(Execution):
    """Fractions can be instantiated."""

    def test_attributes(self, test_execution, verbosity):
        """Both numerator and denominator can be passed."""
        case, fractions = test_execution

        if case.raises:
            assert isinstance(fractions, Exception)
        else:
            assert len({reduce(f.numerator, f.denominator) for f in fractions}) == 1

    def test_default_denominator(self, test_execution, verbosity):
        """The default denominator is 1."""
        case, fractions = test_execution

        if case.raises:
            assert isinstance(fractions, Exception)
        else:
            assert len({(f.numerator, f.denominator) for f in fractions}) == 1


class TestDisplay(Execution):
    """Fractions can be displayed."""

    def test_representation(self, submission, cases, verbosity):
        """`repr` can be used for re-instantiation."""
        Fraction = submission
        f = Fraction(*cases.inputs[0], **cases.inputs[1])
        g = eval(repr(f))
        assert (f.numerator, f.denominator) == (g.numerator, g.denominator)
        # we don't case about the actual values, it should just be idempotent.
    
    def test_string(self, submission, cases, verbosity):
        """`str` creates a string."""
        Fraction = submission
        f = Fraction(*cases.inputs[0], **cases.inputs[1])
        numerator, denominator = map(int, str(f).split(' / '))
        assert (f.numerator, f.denominator) == (numerator, denominator)
        # we don't case about the actual values, it should just be idempotent.
    
    def test_numeric(self, test_execution, verbosity):
        """`.numeric` is a read-only *property* with correct value."""
        case, (fraction,) = test_execution
        with pytest.raises(Exception):
            fraction.numeric = 1.0
        np.testing.assert_almost_equal(fraction.numeric, case.expected[0])


class TestArithmetics(Execution):
    """Fractions implement arithmetic methods."""

    def test_reciprocal(self, test_execution, verbosity):
        """Can `.invert` correctly."""
        case, (fraction,) = test_execution
        if case.raises:
            with pytest.raises(Exception):
                fraction.invert()
        else:
            inverse = fraction.invert()
            np.testing.assert_almost_equal(
                reduce(fraction.numerator, fraction.denominator),
                reduce(inverse.denominator, inverse.numerator),
            )

    def test_add(self, test_execution, verbosity):
        """Can add two instances correctly."""
        case, (a, b) = test_execution
        actual = a + b
        np.testing.assert_allclose(
            reduce(actual.numerator, actual.denominator),
            reduce(*case.expected[0]),
        )

    def test_subtract(self, test_execution, submission):
        """Can subtract two instances correctly."""
        case, (a, b) = test_execution
        actual = a - b
        np.testing.assert_allclose(
            reduce(actual.numerator, actual.denominator),
            reduce(*case.expected[0]),
        )

    def test_multiply(self, test_execution, submission):
        """Can multiply two instances correctly."""
        case, (a, b) = test_execution
        actual = a * b
        np.testing.assert_allclose(
            reduce(actual.numerator, actual.denominator),
            reduce(*case.expected[0]),
        )

    def test_divide(self, test_execution, submission):
        """Can divide two instances correctly."""
        case, (a, b) = test_execution
        if case.raises:
            with pytest.raises(Exception):
                a / b
        else:
            actual = a / b
            np.testing.assert_allclose(
                reduce(actual.numerator, actual.denominator),
                reduce(*case.expected[0]),
            )


class TestComparison(Execution):
    """Fractions can be compared."""

    def test_lt(self, test_execution, verbosity) -> Enum:
        """Run assertions against results of test execution (pytest fixture)."""
        case, (a, b) = test_execution
        np.testing.assert_equal(a < b, *case.expected[0])

    def test_le(self, test_execution, verbosity) -> Enum:
        """Run assertions against results of test execution (pytest fixture)."""
        case, (a, b) = test_execution
        np.testing.assert_equal(a <= b, *case.expected[0])

    def test_ge(self, test_execution, verbosity) -> Enum:
        """Run assertions against results of test execution (pytest fixture)."""
        case, (a, b) = test_execution
        np.testing.assert_equal(a >= b, *case.expected[0])

    def test_gt(self, test_execution, verbosity) -> Enum:
        """Run assertions against results of test execution (pytest fixture)."""
        case, (a, b) = test_execution
        np.testing.assert_equal(a > b, *case.expected[0])

    def test_eq(self, test_execution, verbosity) -> Enum:
        """Run assertions against results of test execution (pytest fixture)."""
        case, (a, b) = test_execution
        np.testing.assert_equal(a == b, *case.expected[0])

    def test_ne(self, test_execution, verbosity) -> Enum:
        """Run assertions against results of test execution (pytest fixture)."""
        case, (a, b) = test_execution
        np.testing.assert_equal(a != b, *case.expected[0])
