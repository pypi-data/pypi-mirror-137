from baby_steps import given, then, when
from district42 import from_native, schema
from jj.mock import HistoryResponse
from revolt import substitute
from th import PathHolder
from valera import validate
from valera.errors import SchemaMismatchValidationError, TypeValidationError, ValueValidationError

from jj_district42 import HistoryResponseSchema

from ._utils import make_history_response


def test_response_history_type_validation():
    with given:
        sch = HistoryResponseSchema()
        resp = make_history_response()

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_type_validation_error():
    with given:
        sch = HistoryResponseSchema()
        resp = make_history_response()
        val = resp.to_dict()

    with when:
        result = validate(sch, val)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), val, HistoryResponse)
        ]


def test_response_history_status_validation():
    with given:
        status = 200
        sch = substitute(HistoryResponseSchema(), {"status": status})
        resp = make_history_response(status=status)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_status_validation_error():
    with given:
        expected_status, actual_status = 200, 404
        sch = substitute(HistoryResponseSchema(), {"status": expected_status})
        resp = make_history_response(status=actual_status)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["status"], actual_status, expected_status)
        ]


def test_response_history_reason_validation():
    with given:
        reason = "OK"
        sch = substitute(HistoryResponseSchema(), {"reason": reason})
        resp = make_history_response(reason=reason)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_reason_validation_error():
    with given:
        expected_reason, actual_reason = "OK", "NOT FOUND"
        sch = substitute(HistoryResponseSchema(), {"reason": expected_reason})
        resp = make_history_response(reason=actual_reason)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["reason"], actual_reason, expected_reason)
        ]


def test_response_history_body_binary_validation():
    with given:
        body = b"200 OK"
        sch = substitute(HistoryResponseSchema(), {"body": body})
        resp = make_history_response(body=body)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_body_binary_validation_error():
    with given:
        expected_body, actual_body = b"200 OK", b"404 NOT FOUND"
        sch = substitute(HistoryResponseSchema(), {"body": expected_body})
        resp = make_history_response(body=actual_body)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(PathHolder()["body"],
                                          actual_body,
                                          (schema.bytes(expected_body),))
        ]


def test_response_history_body_validation():
    with given:
        body = [{"id": 1, "name": "Bob"}]
        sch = substitute(HistoryResponseSchema(), {"body": body})
        resp = make_history_response(body=body)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_body_validation_error():
    with given:
        expected_body = {"id": 1, "name": "Bob"}
        actual_body = {"id": 1, "name": "Alice"}
        sch = substitute(HistoryResponseSchema(), {"body": expected_body})
        resp = make_history_response(body=actual_body)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(PathHolder()["body"],
                                          actual_body,
                                          (from_native(expected_body),))
        ]


def test_response_history_raw_validation():
    with given:
        raw = b"200 OK"
        sch = substitute(HistoryResponseSchema(), {"raw": raw})
        resp = make_history_response(raw=raw)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_raw_validation_error():
    with given:
        expected_raw, actual_raw = b"200 OK", b"404 NOT FOUND"
        sch = substitute(HistoryResponseSchema(), {"raw": expected_raw})
        resp = make_history_response(raw=actual_raw)

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["raw"], actual_raw, expected_raw)
        ]


def test_response_history_validation():
    with given:
        resp = make_history_response(status=200, reason="OK")
        sch = HistoryResponseSchema()

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == []


def test_response_history_validation_error():
    with given:
        status, reason = 200, "OK"
        sch = substitute(HistoryResponseSchema(), {"status": status, "reason": reason})
        resp = make_history_response(status=status, reason="")

    with when:
        result = validate(sch, resp)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["reason"], "", reason)
        ]


def test_response_history_nested():
    with given:
        sch = schema.list([HistoryResponseSchema()])
        resp = make_history_response()

    with when:
        result = validate(sch, [resp])

    with then:
        assert result.get_errors() == []
