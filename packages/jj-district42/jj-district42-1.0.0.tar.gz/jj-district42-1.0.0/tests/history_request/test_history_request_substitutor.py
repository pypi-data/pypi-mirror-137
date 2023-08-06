from baby_steps import given, then, when
from district42 import schema
from multidict import CIMultiDict, MultiDict
from pytest import raises
from revolt import substitute
from revolt.errors import SubstitutionError

from jj_district42 import HistoryRequestSchema
from jj_district42.history_request import RequestSchema

from ._utils import make_history_request


def test_history_request_empty_dict_substitution():
    with given:
        sch = HistoryRequestSchema()

    with when:
        res = substitute(sch, {})

    with then:
        assert isinstance(res, HistoryRequestSchema)
        assert id(res) != id(sch)


def test_history_request_incorrect_type_substitution_error():
    with given:
        sch = HistoryRequestSchema()

    with when, raises(Exception) as exception:
        substitute(sch, set())

    with then:
        assert exception.type is SubstitutionError


def test_history_request_dict_substitution():
    with given:
        req = {
            "method": "GET",
            "path": "/users",
            "segments": {},
            "params": {"user_id": "1"},
            "headers": {"Authorization": "banana"},
            "body": [],
            "raw": b"[]",
        }
        sch = HistoryRequestSchema()

    with when:
        res = substitute(sch, req)

    with then:
        assert res.props.type == substitute(RequestSchema, req)
        assert id(res) != id(sch)


def test_history_request_req_substitution():
    with given:
        req = {
            "method": "GET",
            "path": "/users",
            "segments": {},
            "params": {"user_id": "1"},
            "headers": {"Authorization": "banana"},
            "body": [],
            "raw": b"[]",
        }
        history_request = make_history_request(
            method=req["method"],
            path=req["path"],
            segments=req["segments"],
            params=MultiDict(req["params"]),
            headers=CIMultiDict(req["headers"]),
            body=req["body"],
            raw=req["raw"],
        )
        sch = HistoryRequestSchema()

    with when:
        res = substitute(sch, history_request)

    with then:
        assert res.props.type == substitute(RequestSchema, req)
        assert id(res) != id(sch)


def test_history_request_inner_dict_substitution():
    with given:
        sch = schema.dict({
            "request": HistoryRequestSchema()
        })

    with when:
        res = substitute(sch, {
            "request": {}
        })

    with then:
        assert isinstance(res["request"], HistoryRequestSchema)
        assert id(res) != id(sch)


def test_history_request_inner_req_substitution():
    with given:
        sch = schema.dict({
            "request": HistoryRequestSchema()
        })
        req = make_history_request()

    with when:
        res = substitute(sch, {
            "request": req
        })

    with then:
        assert isinstance(res["request"], HistoryRequestSchema)
        assert id(res) != id(sch)
