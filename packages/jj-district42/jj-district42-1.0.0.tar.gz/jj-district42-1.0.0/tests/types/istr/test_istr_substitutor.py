from typing import Callable

import pytest
from baby_steps import given, then, when
from pytest import raises
from revolt import substitute
from revolt.errors import SubstitutionError

from jj_district42.types.istr import IStrSchema


def test_istr_substitution():
    with given:
        value = "banana"
        sch = IStrSchema()

    with when:
        res = substitute(sch, value)

    with then:
        assert res == IStrSchema()(value)
        assert res != sch


@pytest.mark.parametrize("modifier", [str, str.lower, str.upper])
def test_istr_value_substitution(modifier: Callable[[str], str]):
    with given:
        value = "Banana"
        sch = IStrSchema()(value)

    with when:
        res = substitute(sch, modifier(value))

    with then:
        assert res == IStrSchema()(modifier(value))
        assert id(res) != id(sch)


def test_istr_substitution_invalid_value_error():
    with given:
        value = "banana"
        sch = IStrSchema()(value)

    with when, raises(Exception) as exception:
        substitute(sch, ["b", "a", "n", "a", "n", "a"])

    with then:
        assert exception.type is SubstitutionError


def test_istr_substitution_incorrect_value_error():
    with given:
        value = "banana"
        sch = IStrSchema()(value)

    with when, raises(Exception) as exception:
        substitute(sch, "apple")

    with then:
        assert exception.type is SubstitutionError
