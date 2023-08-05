from typing import Any

from blahblah import Generator
from jj.mock import HistoryRequest

from ._history_request_schema import HistoryRequestSchema

__all__ = ("HistoryRequestGenerator",)


class HistoryRequestGenerator(Generator, extend=True):
    def visit_jj_history_request(self,
                                 schema: HistoryRequestSchema,
                                 **kwargs: Any) -> HistoryRequest:
        generated = self.visit_type_alias(schema, **kwargs)
        return HistoryRequest(**generated)
