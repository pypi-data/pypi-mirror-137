from baby_steps import given, then, when
from district42 import represent

from jj_district42.types.istr import IStrSchema


def test_istr_representation():
    with given:
        sch = IStrSchema()

    with when:
        res = represent(sch)

    with then:
        assert res == "schema.istr"


def test_istr_value_representation():
    with given:
        value = "Banana"
        sch = IStrSchema()(value)

    with when:
        res = represent(sch)

    with then:
        assert res == f"schema.istr({value!r})"
