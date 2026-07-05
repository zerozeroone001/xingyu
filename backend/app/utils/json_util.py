from __future__ import annotations

import json
from typing import Any


def parse_json_list(value: str | None) -> list[Any]:
    if not value:
        return []
    try:
        data = json.loads(value)
    except json.JSONDecodeError:
        return []
    return data if isinstance(data, list) else []


def dump_json_list(value: list[Any] | None) -> str:
    return json.dumps(value or [], ensure_ascii=False)
