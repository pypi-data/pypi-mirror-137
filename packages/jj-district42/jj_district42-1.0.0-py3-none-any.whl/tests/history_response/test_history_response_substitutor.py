from baby_steps import given, then, when
from district42 import schema
from multidict import CIMultiDict
from pytest import raises
from revolt import substitute
from revolt.errors import SubstitutionError

from jj_district42 import HistoryResponseSchema
from jj_district42.history_response import ResponseSchema

from ._utils import make_history_response


def test_history_response_empty_dict_substitution():
    with given:
        sch = HistoryResponseSchema()

    with when:
        res = substitute(sch, {})

    with then:
        assert isinstance(res, HistoryResponseSchema)
        assert id(res) != id(sch)


def test_history_response_incorrect_type_substitution_error():
    with given:
        sch = HistoryResponseSchema()

    with when, raises(Exception) as exception:
        substitute(sch, set())

    with then:
        assert exception.type is SubstitutionError


def test_history_response_dict_substitution():
    with given:
        resp = {
            "status": 200,
            "reason": "OK",
            "headers": {"Authorization": "banana"},
            "body": [],
            "raw": b"[]",
        }
        sch = HistoryResponseSchema()

    with when:
        res = substitute(sch, resp)

    with then:
        assert res.props.type == substitute(ResponseSchema, resp)
        assert id(res) != id(sch)


def test_history_response_resp_substitution():
    with given:
        resp = {
            "status": 200,
            "reason": "OK",
            "headers": {"Authorization": "banana"},
            "body": [],
            "raw": b"[]",
        }
        history_response = make_history_response(
            status=resp["status"],
            reason=resp["reason"],
            headers=CIMultiDict(resp["headers"]),
            body=resp["body"],
            raw=resp["raw"],
        )
        sch = HistoryResponseSchema()

    with when:
        res = substitute(sch, history_response)

    with then:
        assert res.props.type == substitute(ResponseSchema, resp)
        assert id(res) != id(sch)


def test_history_response_inner_dict_substitution():
    with given:
        sch = schema.dict({
            "response": HistoryResponseSchema()
        })

    with when:
        res = substitute(sch, {
            "response": {}
        })

    with then:
        assert isinstance(res["response"], HistoryResponseSchema)
        assert id(res) != id(sch)


def test_history_response_inner_resp_substitution():
    with given:
        sch = schema.dict({
            "response": HistoryResponseSchema()
        })
        resp = make_history_response()

    with when:
        res = substitute(sch, {
            "response": resp
        })

    with then:
        assert isinstance(res["response"], HistoryResponseSchema)
        assert id(res) != id(sch)
