from baby_steps import then, when

from jj_district42.types.param_list import ParamListSchema


def test_param_list_declaration():
    with when:
        sch = ParamListSchema()

    with then:
        assert isinstance(sch, ParamListSchema)
