from baby_steps import given, then, when
from blahblah import fake

from jj_district42.types.header_list import HeaderListSchema


def test_header_list_generation():
    with given:
        sch = HeaderListSchema()

    with when:
        res = fake(sch)

    with then:
        assert isinstance(res, list)
