from __future__ import annotations

from typing import Any


def success(data: Any = None, message: str = "success") -> dict[str, Any]:
    return {
        "code": 0,
        "message": message,
        "data": {} if data is None else data,
    }


def error(code: int, message: str, data: Any = None) -> dict[str, Any]:
    return {
        "code": code,
        "message": message,
        "data": {} if data is None else data,
    }
