from typing import Any, cast

from district42 import SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42 import schema
from district42.types import DictSchema, GenericTypeAliasSchema, TypeAliasProps

from jj_district42.types.header_list import HeaderListSchema

__all__ = ("HistoryResponseSchema", "HistoryResponseProps", "ResponseSchema",)


ResponseSchema = schema.dict({
    "status": schema.int,
    "reason": schema.str,
    "headers": HeaderListSchema(),
    "body": schema.any
})


class HistoryResponseProps(TypeAliasProps):
    @property
    def type(self) -> DictSchema:
        return cast(DictSchema, self.get("type", ResponseSchema))


class HistoryResponseSchema(GenericTypeAliasSchema[HistoryResponseProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        try:
            return cast(ReturnType, visitor.visit_jj_history_response(self, **kwargs))
        except AttributeError:
            return visitor.visit_type_alias(self, **kwargs)
