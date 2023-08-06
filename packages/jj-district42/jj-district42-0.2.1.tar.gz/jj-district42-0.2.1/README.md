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
import jj
import httpx
from jj.mock import mocked
from jj_district42 import HistorySchema
from valera import validate_or_fail


matcher = jj.match("GET", "/users")
response = jj.Response(status=200, json=[])

with mocked(matcher, response) as mock:
    resp = httpx.get("http://localhost:8080/users", params={"user_id": 1})

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
```
