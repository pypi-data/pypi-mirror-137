from typing import Any

from jj.mock import HistoryResponse
from niltype import Nil, Nilable
from th import PathHolder
from valera import ValidationResult, Validator

from ._history_response_schema import HistoryResponseSchema

__all__ = ("HistoryResponseValidator",)


class HistoryResponseValidator(Validator, extend=True):
    def visit_jj_history_response(self, schema: HistoryResponseSchema, *,
                                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                                  **kwargs: Any) -> ValidationResult:
        result = self._validation_result_factory()
        if path is Nil:
            path = self._path_holder_factory()

        if error := self._validate_type(path, value, HistoryResponse):
            return result.add_error(error)

        return self.visit_type_alias(schema, value=value.to_dict(), path=path, **kwargs)
