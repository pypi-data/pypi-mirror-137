from baby_steps import given, then, when
from district42 import schema
from district42_exp_types.unordered import unordered_schema
from pytest import raises
from revolt import substitute
from revolt.errors import SubstitutionError

from jj_district42.types.header_list import HeaderListSchema
from jj_district42.types.istr import IStrSchema


def test_header_list_empty_list_substitution():
    with given:
        sch = HeaderListSchema()

    with when:
        res = substitute(sch, [])

    with then:
        assert res.props.type == unordered_schema([])
        assert res != sch


def test_header_list_list_substitution():
    with given:
        value = [["key", "val"]]
        sch = HeaderListSchema()

    with when:
        res = substitute(sch, value)

    with then:
        assert res.props.type == unordered_schema([
            schema.list([IStrSchema()("key"), schema.str("val")])
        ])
        assert res != sch


def test_header_list_list_multiple_substitution():
    with given:
        value = [["key", "val"], ["key", "another_val"]]
        sch = HeaderListSchema()

    with when:
        res = substitute(sch, value)

    with then:
        assert res.props.type == unordered_schema([
            schema.list([IStrSchema()("key"), schema.str("val")]),
            schema.list([IStrSchema()("key"), schema.str("another_val")])
        ])
        assert res != sch


def test_header_list_empty_dict_substitution():
    with given:
        sch = HeaderListSchema()

    with when:
        res = substitute(sch, {})

    with then:
        assert res.props.type == unordered_schema([])
        assert res != sch


def test_header_list_dict_substitution():
    with given:
        value = {"key": "val"}
        sch = HeaderListSchema()

    with when:
        res = substitute(sch, value)

    with then:
        assert res.props.type == unordered_schema([
            schema.list([IStrSchema()("key"), schema.str("val")])
        ])
        assert res != sch


def test_header_list_dict_multiple_substitution():
    with given:
        value = {"key": "val", "another_key": "val"}
        sch = HeaderListSchema()

    with when:
        res = substitute(sch, value)

    with then:
        assert res.props.type == unordered_schema([
            schema.list([IStrSchema()("key"), schema.str("val")]),
            schema.list([IStrSchema()("another_key"), schema.str("val")])
        ])
        assert res != sch


def test_header_list_incorrect_type_substitution_error():
    with given:
        sch = HeaderListSchema()

    with when, raises(Exception) as exception:
        substitute(sch, set())

    with then:
        assert exception.type is SubstitutionError


def test_header_list_incorrect_dict_value_substitution_error():
    with given:
        sch = HeaderListSchema()

    with when, raises(Exception) as exception:
        substitute(sch, {"key": None})

    with then:
        assert exception.type is SubstitutionError


def test_header_list_incorrect_list_value_substitution_error():
    with given:
        sch = HeaderListSchema()

    with when, raises(Exception) as exception:
        substitute(sch, [[]])

    with then:
        assert exception.type is SubstitutionError
