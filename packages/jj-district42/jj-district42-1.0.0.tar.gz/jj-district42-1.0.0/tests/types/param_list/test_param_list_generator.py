from baby_steps import given, then, when
from blahblah import fake

from jj_district42.types.param_list import ParamListSchema


def test_param_list_generation():
    with given:
        sch = ParamListSchema()

    with when:
        res = fake(sch)

    with then:
        assert isinstance(res, list)
