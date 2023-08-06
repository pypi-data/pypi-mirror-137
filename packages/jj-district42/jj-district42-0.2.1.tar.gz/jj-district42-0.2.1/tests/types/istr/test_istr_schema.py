from uuid import uuid4

from baby_steps import given, then, when
from district42.errors import DeclarationError
from pytest import raises

from jj_district42.types.istr import IStrSchema


def test_istr_declaration():
    with when:
        sch = IStrSchema()

    with then:
        assert isinstance(sch, IStrSchema)


def test_istr_value_declaration():
    with given:
        value = str(uuid4())

    with when:
        sch = IStrSchema()(value)

    with then:
        assert sch.props.value == value


def test_istr_invalid_value_type_declaration_error():
    with given:
        value = ["b", "a", "n", "a", "n", "a"]

    with when, raises(Exception) as exception:
        IStrSchema()(value)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == ("`schema.istr` value must be an instance of 'str', "
                                        f"instance of 'list' {value!r} given")


def test_istr_already_declared_declaration_error():
    with given:
        value = "banana"
        another_value = "apple"

    with when, raises(Exception) as exception:
        IStrSchema()(value)(another_value)

    with then:
        assert exception.type is DeclarationError
        assert str(exception.value) == f"`schema.istr({value!r})` is already declared"
