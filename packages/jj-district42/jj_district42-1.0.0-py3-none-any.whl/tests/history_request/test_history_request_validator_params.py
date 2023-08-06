from baby_steps import given, then, when
from district42 import schema
from district42_exp_types.unordered import UnorderedContainsValidationError
from multidict import MultiDict
from revolt import substitute
from th import PathHolder
from valera import validate
from valera.errors import ExtraElementValidationError

from jj_district42 import HistoryRequestSchema

from ._utils import make_history_request


def test_request_history_no_params_validation():
    with given:
        sch = HistoryRequestSchema()
        params = {"user_id": "1"}
        req = make_history_request(params=MultiDict(params))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_dict_params_validation():
    with given:
        params = {"user_id": "1"}
        sch = substitute(HistoryRequestSchema(), {"params": params})
        req = make_history_request(params=MultiDict(params))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_dict_params_case_validation_error():
    with given:
        actual_params = {"User_Id": "1"}
        expected_params = {"user_id": "1"}
        sch = substitute(HistoryRequestSchema(), {"params": expected_params})
        req = make_history_request(params=MultiDict(actual_params))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["params"], schema.list([
                schema.str("user_id"),
                schema.str("1")
            ])),
            ExtraElementValidationError(PathHolder()["params"], ["User_Id", "1"], 0)
        ]


def test_request_history_list_params_validation():
    with given:
        params = [["user_id", "1"]]
        sch = substitute(HistoryRequestSchema(), {"params": params})
        req = make_history_request(params=MultiDict(params))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_list_multiple_params_validation():
    with given:
        params = [["user_id", "1"], ["user_id", "2"]]
        sch = substitute(HistoryRequestSchema(), {"params": params})
        req = make_history_request(params=MultiDict(params))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == []


def test_request_history_dict_params_validation_error():
    with given:
        expected_params = {"user_id": "1"}
        actual_params = {"user_id": "2"}
        sch = substitute(HistoryRequestSchema(), {"params": expected_params})
        req = make_history_request(params=MultiDict(actual_params))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["params"], schema.list([
                schema.str("user_id"),
                schema.str("1")
            ])),
            ExtraElementValidationError(PathHolder()["params"], ["user_id", "2"], 0)
        ]


def test_request_history_list_params_validation_error():
    with given:
        expected_params = [["user_id", "1"]]
        actual_params = [["user_id", "2"]]
        sch = substitute(HistoryRequestSchema(), {"params": expected_params})
        req = make_history_request(params=MultiDict(actual_params))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["params"], schema.list([
                schema.str("user_id"),
                schema.str("1")
            ])),
            ExtraElementValidationError(PathHolder()["params"], ["user_id", "2"], 0),
        ]


def test_request_history_list_multiple_params_validation_error():
    with given:
        expected_params = [["user_id", "1"], ["user_id", "2"]]
        actual_params = [["user_id", "1"]]
        sch = substitute(HistoryRequestSchema(), {"params": expected_params})
        req = make_history_request(params=MultiDict(actual_params))

    with when:
        result = validate(sch, req)

    with then:
        assert result.get_errors() == [
            UnorderedContainsValidationError(PathHolder()["params"], schema.list([
                schema.str("user_id"),
                schema.str("2")
            ])),
        ]
