from baby_steps import given, then, when
from blahblah import fake

from jj_district42.types.istr import IStrSchema


def test_istr_generation():
    with given:
        sch = IStrSchema()

    with when:
        res = fake(sch)

    with then:
        assert isinstance(res, str)


def test_istr_value_generation():
    with given:
        value = "banana"
        sch = IStrSchema()(value)

    with when:
        res = fake(sch)

    with then:
        assert res in (value, value.lower(), value.upper())
