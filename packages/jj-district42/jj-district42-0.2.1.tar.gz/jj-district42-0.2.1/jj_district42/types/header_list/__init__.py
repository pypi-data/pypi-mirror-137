from typing import Any, cast

from district42 import SchemaVisitor
from district42 import SchemaVisitorReturnType as ReturnType
from district42 import schema as sch
from district42.types import DictSchema, GenericTypeAliasSchema, TypeAliasProps
from district42_exp_types.unordered import unordered_schema
from niltype import Nil, Nilable
from revolt import Substitutor
from th import PathHolder
from valera import ValidationResult, Validator

from jj_district42.types.istr import IStrSchema

__all__ = ("HeaderListSchema", "HeaderListProps",
           "HeaderListSubstitutor", "HeaderListValidator",)


class HeaderListProps(TypeAliasProps):
    @property
    def type(self) -> DictSchema:
        key_val = sch.list([IStrSchema(), sch.str])
        type_ = self.get("type", unordered_schema(key_val))
        return cast(DictSchema, type_)


class HeaderListSchema(GenericTypeAliasSchema[HeaderListProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        try:
            return cast(ReturnType, visitor.visit_jj_header_list(self, **kwargs))
        except AttributeError:
            return visitor.visit_type_alias(self, **kwargs)


class HeaderListSubstitutor(Substitutor, extend=True):
    def visit_jj_header_list(self, schema: HeaderListSchema, *,
                             value: Any = Nil, **kwargs: Any) -> HeaderListSchema:
        if isinstance(value, dict):
            value = [[key, val] for key, val in value.items()]
        return cast(HeaderListSchema, self.visit_type_alias(schema, value=value, **kwargs))


class HeaderListValidator(Validator, extend=True):
    def visit_jj_header_list(self, schema: HeaderListSchema, *,
                             value: Any = Nil, path: Nilable[PathHolder] = Nil,
                             **kwargs: Any) -> ValidationResult:
        if isinstance(value, dict):
            value = [[key, val] for key, val in value.items()]
        return self.visit_type_alias(schema, value=value, path=path, **kwargs)
