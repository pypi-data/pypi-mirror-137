from baby_steps import given, then, when
from district42 import represent

from jj_district42 import HistoryRequestSchema


def test_history_request_representation():
    with given:
        sch = HistoryRequestSchema()

    with when:
        res = represent(sch)

    with then:
        assert res == "\n".join([
            "HistoryRequestSchema<schema.dict({",
            "    'method': schema.str.len(1, ...),",
            "    'path': schema.str,",
            "    'segments': schema.dict,",
            "    'params': ParamListSchema<schema.unordered(schema.list([",
            "        schema.str,",
            "        schema.str",
            "    ]))>,",
            "    'headers': HeaderListSchema<schema.unordered(schema.list([",
            "        schema.istr,",
            "        schema.str",
            "    ]))>,",
            "    'body': schema.any,",
            "    'raw': schema.bytes",
            "})>",
        ])
