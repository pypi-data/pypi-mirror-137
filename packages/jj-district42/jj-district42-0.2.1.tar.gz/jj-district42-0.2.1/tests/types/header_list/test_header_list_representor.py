from baby_steps import given, then, when
from district42 import represent

from jj_district42.types.header_list import HeaderListSchema


def test_header_list_representation():
    with given:
        sch = HeaderListSchema()

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "HeaderListSchema<schema.unordered(schema.list([",
            "    schema.istr,",
            "    schema.str",
            "]))>",
        ])
