from typing import Any, cast

from jj.mock import HistoryResponse
from niltype import Nil, Nilable
from revolt import Substitutor, SubstitutorValidator
from th import PathHolder
from valera import ValidationResult

from ._history_response_schema import HistoryResponseSchema

__all__ = ("HistoryResponseSubstitutor", "HistoryResponseSubstitutorValidator",)


class HistoryResponseSubstitutor(Substitutor, extend=True):
    def visit_jj_history_response(self, schema: HistoryResponseSchema, *,
                                  value: Any = Nil, **kwargs: Any) -> HistoryResponseSchema:
        if isinstance(value, HistoryResponse):
            value = value.to_dict()
        return cast(HistoryResponseSchema, self.visit_type_alias(schema, value=value, **kwargs))


class HistoryResponseSubstitutorValidator(SubstitutorValidator, extend=True):
    def visit_jj_history_response(self, schema: HistoryResponseSchema, *,
                                  value: Any = Nil, path: Nilable[PathHolder] = Nil,
                                  **kwargs: Any) -> ValidationResult:
        if isinstance(value, HistoryResponse):
            value = value.to_dict()
        return self.visit_type_alias(schema, value=value, path=path, **kwargs)
