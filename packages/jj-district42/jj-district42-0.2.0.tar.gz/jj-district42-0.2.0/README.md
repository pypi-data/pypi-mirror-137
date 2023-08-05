# jj-district42

[![Codecov](https://img.shields.io/codecov/c/github/nikitanovosibirsk/jj-district42/master.svg?style=flat-square)](https://codecov.io/gh/nikitanovosibirsk/jj-district42)
[![PyPI](https://img.shields.io/pypi/v/jj-district42.svg?style=flat-square)](https://pypi.python.org/pypi/jj-district42/)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/jj-district42?style=flat-square)](https://pypi.python.org/pypi/jj-district42/)
[![Python Version](https://img.shields.io/pypi/pyversions/jj-district42.svg?style=flat-square)](https://pypi.python.org/pypi/jj-district42/)


## Installation

```sh
pip3 install jj-district42
```

## Usage

```python
import asyncio
import jj
from httpx import AsyncClient
from jj.mock import mocked
from jj_district42 import HistorySchema
from valera import validate_or_fail

async def main():
    matcher = jj.match("GET", "/users")
    response = jj.Response(status=200, json=[])

    async with mocked(matcher, response) as mock:
        async with AsyncClient() as client:
            params = {"user_id": 1}
            await client.get("http://localhost:8080/users", params=params)

    assert validate_or_fail(
        HistorySchema % [
            {
                "request": {
                    "method": "GET",
                    "path": "/users",
                    # equals (exact match)
                    "params": {"user_id": "1"},
                },
                "response": {
                    "status": 200,
                    # contains
                    "headers": [
                        ..., 
                        ["Content-Type", "application/json"],
                        ...
                    ],
                    "body": b"[]",
                }
            }
        ],
        mock.history
    )

asyncio.run(main())
```
