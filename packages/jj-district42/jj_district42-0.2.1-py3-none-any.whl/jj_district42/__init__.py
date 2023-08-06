from district42 import register_type, schema
from district42_exp_types.uuid_str import UUIDStrSchema

from ._version import version
from .history_request import HistoryRequestSchema
from .history_response import HistoryResponseSchema

schema_history_request = register_type("jj_history_request", HistoryRequestSchema)
schema_history_response = register_type("jj_history_response", HistoryResponseSchema)

HistoryItemSchema = schema.dict({
    "request": HistoryRequestSchema(),
    "response": HistoryResponseSchema(),
    "tags": schema.list(UUIDStrSchema()),
})

HistorySchema = schema.list(HistoryItemSchema)

__version__ = version
__all__ = ("HistorySchema", "HistoryItemSchema",
           "schema_history_request", "schema_history_response",
           "HistoryRequestSchema", "HistoryResponseSchema",)
