from baby_steps import given, then, when
from district42 import from_native, schema
from jj.mock import HistoryRequest
from revolt import substitute
from th import PathHolder
from valera import validate
from valera.errors import SchemaMismatchValidationError, TypeValidationError, ValueValidationError

from jj_district42 import HistoryRequestSchema

from ._utils import make_history_request


def test_request_history_type_validation():
    with given:
        sch = HistoryRequestSchema()
        req = make_history_request()

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_type_validation_error():
    with given:
        sch = HistoryRequestSchema()
        req = make_history_request()
        val = req.to_dict()

    with when:
        result = validate(sch, val)

    with then:
        assert result.get_errors() == [
            TypeValidationError(PathHolder(), val, HistoryRequest)
        ]


def test_request_history_method_validation():
    with given:
        method = "GET"
        sch = substitute(HistoryRequestSchema(), {"method": method})
        req = make_history_request(method=method)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_method_validation_error():
    with given:
        expected_method, actual_method = "GET", "POST"
        sch = substitute(HistoryRequestSchema(), {"method": expected_method})
        req = make_history_request(method=actual_method)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["method"], actual_method, expected_method)
        ]


def test_request_history_path_validation():
    with given:
        path = "/users"
        sch = substitute(HistoryRequestSchema(), {"path": path})
        req = make_history_request(path=path)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_path_validation_error():
    with given:
        expected_path, actual_path = "/users", "/"
        sch = substitute(HistoryRequestSchema(), {"path": expected_path})
        req = make_history_request(path=actual_path)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["path"], actual_path, expected_path)
        ]


def test_request_history_segments_validation():
    with given:
        segments = {"user_id": "1"}
        sch = substitute(HistoryRequestSchema(), {"segments": segments})
        req = make_history_request(segments=segments)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_segments_validation_error():
    with given:
        expected_segments = {"user_id": "1"}
        actual_segments = {"user_id": "2"}
        sch = substitute(HistoryRequestSchema(), {"segments": expected_segments})
        req = make_history_request(segments=actual_segments)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["segments"]["user_id"],
                                 actual_segments["user_id"],
                                 expected_segments["user_id"])
        ]


def test_request_history_body_binary_validation():
    with given:
        body = b""
        sch = substitute(HistoryRequestSchema(), {"body": body})
        req = make_history_request(body=body)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_body_binary_validation_error():
    with given:
        expected_body, actual_body = b"<expected>", b"<actual>"
        sch = substitute(HistoryRequestSchema(), {"body": expected_body})
        req = make_history_request(body=actual_body)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(PathHolder()["body"],
                                          actual_body,
                                          (schema.bytes(expected_body),))
        ]


def test_request_history_body_validation():
    with given:
        body = [{"id": 1, "name": "Bob"}]
        sch = substitute(HistoryRequestSchema(), {"body": body})
        req = make_history_request(body=body)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_body_validation_error():
    with given:
        expected_body = {"id": 1, "name": "Bob"}
        actual_body = {"id": 1, "name": "Alice"}
        sch = substitute(HistoryRequestSchema(), {"body": expected_body})
        req = make_history_request(body=actual_body)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            SchemaMismatchValidationError(PathHolder()["body"],
                                          actual_body,
                                          (from_native(expected_body),))
        ]


def test_request_history_raw_validation():
    with given:
        raw = b""
        sch = substitute(HistoryRequestSchema(), {"raw": raw})
        req = make_history_request(raw=raw)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_raw_validation_error():
    with given:
        expected_raw, actual_raw = b"<expected>", b"<actual>"
        sch = substitute(HistoryRequestSchema(), {"raw": expected_raw})
        req = make_history_request(raw=actual_raw)

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["raw"], actual_raw, expected_raw)
        ]


def test_request_history_validation():
    with given:
        req = make_history_request(method="GET", path="/")
        sch = HistoryRequestSchema()

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_validation_error():
    with given:
        method, path = "GET", "/users"
        sch = substitute(HistoryRequestSchema(), {"method": method, "path": path})
        req = make_history_request(method=method, path="/")

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            ValueValidationError(PathHolder()["path"], "/", path)
        ]


def test_request_history_nested():
    with given:
        sch = schema.list([HistoryRequestSchema()])
        req = make_history_request()

    with when:
        result = validate(sch, [req])

    with then:
        assert result.get_errors() == []
