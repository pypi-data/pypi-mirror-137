from baby_steps import given, then, when
from district42 import schema
from pytest import raises

from jj_district42 import HistoryRequestSchema


def test_history_request_declaration():
    with when:
        sch = HistoryRequestSchema()

    with then:
        assert isinstance(sch, HistoryRequestSchema)


def test_history_request_add_declaration():
    with given:
        sch = HistoryRequestSchema()
        added = schema.dict({
            "path": schema.str.contains("/users/")
        })

    with when:
        res = sch + added

    with then:
        assert isinstance(sch, HistoryRequestSchema)
        assert res.props.type == sch.props.type + added


def test_history_request_add_declaration_error():
    with given:
        sch = HistoryRequestSchema()
        added = schema.str

    with when, raises(Exception) as exception:
        sch + added

    with then:
        assert exception.type is AssertionError
