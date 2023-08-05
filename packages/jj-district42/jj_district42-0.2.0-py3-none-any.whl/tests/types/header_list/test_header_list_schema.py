from baby_steps import then, when

from jj_district42.types.header_list import HeaderListSchema


def test_header_list_declaration():
    with when:
        sch = HeaderListSchema()

    with then:
        assert isinstance(sch, HeaderListSchema)
