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

__all__ = ("ParamListSchema", "ParamListProps",
           "ParamListSubstitutor", "ParamListValidator",)


class ParamListProps(TypeAliasProps):
    @property
    def type(self) -> DictSchema:
        key_val = sch.list([sch.str, sch.str])
        type_ = self.get("type", unordered_schema(key_val))
        return cast(DictSchema, type_)


class ParamListSchema(GenericTypeAliasSchema[ParamListProps]):
    def __accept__(self, visitor: SchemaVisitor[ReturnType], **kwargs: Any) -> ReturnType:
        try:
            return cast(ReturnType, visitor.visit_jj_param_list(self, **kwargs))
        except AttributeError:
            return visitor.visit_type_alias(self, **kwargs)


class ParamListSubstitutor(Substitutor, extend=True):
    def visit_jj_param_list(self, schema: ParamListSchema, *,
                            value: Any = Nil, **kwargs: Any) -> ParamListSchema:
        if isinstance(value, dict):
            value = [[key, val] for key, val in value.items()]
        return cast(ParamListSchema, self.visit_type_alias(schema, value=value, **kwargs))


class ParamListValidator(Validator, extend=True):
    def visit_jj_param_list(self, schema: ParamListSchema, *,
                            value: Any = Nil, path: Nilable[PathHolder] = Nil,
                            **kwargs: Any) -> ValidationResult:
        if isinstance(value, dict):
            value = [[key, val] for key, val in value.items()]
        return self.visit_type_alias(schema, value=value, path=path, **kwargs)
