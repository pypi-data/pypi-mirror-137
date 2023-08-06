from baby_steps import given, then, when
from district42 import schema
from district42_exp_types.unordered import UnorderedContainsValidationError
from multidict import CIMultiDict
from revolt import substitute
from th import PathHolder
from valera import validate
from valera.errors import ExtraElementValidationError

from jj_district42 import HistoryRequestSchema
from jj_district42.types.istr import IStrSchema

from ._utils import make_history_request


def test_request_history_no_headers_validation():
    with given:
        sch = HistoryRequestSchema()
        headers = {"user_id": "1"}
        req = make_history_request(headers=CIMultiDict(headers))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_dict_headers_validation():
    with given:
        headers = {"user_id": "1"}
        sch = substitute(HistoryRequestSchema(), {"headers": headers})
        req = make_history_request(headers=CIMultiDict(headers))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_dict_headers_case_validation():
    with given:
        actual_headers = {"User_Id": "1"}
        expected_headers = {"user_id": "1"}
        sch = substitute(HistoryRequestSchema(), {"headers": expected_headers})
        req = make_history_request(headers=CIMultiDict(actual_headers))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_list_headers_validation():
    with given:
        headers = [["user_id", "1"]]
        sch = substitute(HistoryRequestSchema(), {"headers": headers})
        req = make_history_request(headers=CIMultiDict(headers))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_list_multiple_headers_validation():
    with given:
        headers = [["user_id", "1"], ["user_id", "2"]]
        sch = substitute(HistoryRequestSchema(), {"headers": headers})
        req = make_history_request(headers=CIMultiDict(headers))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_dict_headers_validation_error():
    with given:
        expected_headers = {"user_id": "1"}
        actual_headers = {"user_id": "2"}
        sch = substitute(HistoryRequestSchema(), {"headers": expected_headers})
        req = make_history_request(headers=CIMultiDict(actual_headers))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["headers"], schema.list([
                IStrSchema()("user_id"),
                schema.str("1")
            ])),
            ExtraElementValidationError(PathHolder()["headers"], ["user_id", "2"], 0)
        ]


def test_request_history_list_headers_validation_error():
    with given:
        expected_headers = [["user_id", "1"]]
        actual_headers = [["user_id", "2"]]
        sch = substitute(HistoryRequestSchema(), {"headers": expected_headers})
        req = make_history_request(headers=CIMultiDict(actual_headers))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["headers"], schema.list([
                IStrSchema()("user_id"),
                schema.str("1")
            ])),
            ExtraElementValidationError(PathHolder()["headers"], ["user_id", "2"], 0),
        ]


def test_request_history_list_multiple_headers_validation_error():
    with given:
        expected_headers = [["user_id", "1"], ["user_id", "2"]]
        actual_headers = [["user_id", "1"]]
        sch = substitute(HistoryRequestSchema(), {"headers": expected_headers})
        req = make_history_request(headers=CIMultiDict(actual_headers))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["headers"], schema.list([
                IStrSchema()("user_id"),
                schema.str("2")
            ])),
        ]
