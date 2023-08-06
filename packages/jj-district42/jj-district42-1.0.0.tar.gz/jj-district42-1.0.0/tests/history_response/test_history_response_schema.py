from baby_steps import given, then, when
from district42 import schema
from pytest import raises

from jj_district42 import HistoryResponseSchema


def test_history_response_declaration():
    with when:
        sch = HistoryResponseSchema()

    with then:
        assert isinstance(sch, HistoryResponseSchema)


def test_history_response_add_declaration():
    with given:
        sch = HistoryResponseSchema()
        added = schema.dict({
            "reason": schema.str.contains("OK")
        })

    with when:
        res = sch + added

    with then:
        assert isinstance(sch, HistoryResponseSchema)
        assert res.props.type == sch.props.type + added


def test_history_response_add_declaration_error():
    with given:
        sch = HistoryResponseSchema()
        added = schema.str

    with when, raises(Exception) as exception:
        sch + added

    with then:
        assert exception.type is AssertionError
