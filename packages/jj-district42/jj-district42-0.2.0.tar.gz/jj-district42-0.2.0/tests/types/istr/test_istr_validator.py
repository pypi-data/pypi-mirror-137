from typing import Callable

import pytest
from baby_steps import given, then, when
from district42 import schema
from th import PathHolder
from valera import validate
from valera.errors import TypeValidationError, ValueValidationError

from jj_district42.types.istr import IStrSchema


@pytest.mark.parametrize("modifier", [str, str.lower, str.upper])
def test_istr_type_validation(modifier: Callable[[str], str]):
    with given:
        value = modifier("Banana")

    with when:
        result = validate(IStrSchema(), value)

    with then:
        assert result.get_errors() == []


def test_istr_type_validation_error():
    with given:
        value = ["b", "a", "n", "a", "n", "a"]

    with when:
        result = validate(IStrSchema(), value)

    with then:
        assert result.get_errors() == [TypeValidationError(PathHolder(), value, str)]


@pytest.mark.parametrize(("actual_func", "expected_func"), [
    (str.lower, str.upper),
    (str.upper, str.lower),
])
def test_istr_value_validation(actual_func: Callable[[str], str],
                               expected_func: Callable[[str], str]):
    with given:
        value = "banana"
        sch = IStrSchema()(expected_func(value))

    with when:
        result = validate(sch, actual_func(value))

    with then:
        assert result.get_errors() == []


def test_istr_value_validation_error():
    with given:
        expected_value = "banana"
        actual_value = "apple"

    with when:
        result = validate(IStrSchema()(expected_value), actual_value)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder(), actual_value, expected_value)
        ]


def test_istr_nested_validation():
    with given:
        value = "banana"
        sch = schema.list([IStrSchema()(value)])

    with when:
        result = validate(sch, [value])

    with then:
        assert result.get_errors() == []
