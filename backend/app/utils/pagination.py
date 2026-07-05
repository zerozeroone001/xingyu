from __future__ import annotations

from collections.abc import Sequence
from typing import Any

from sqlalchemy import func, select
from sqlalchemy.orm import Session


def clamp_page(page: int) -> int:
    return max(1, int(page or 1))


def clamp_page_size(page_size: int) -> int:
    return min(100, max(1, int(page_size or 10)))


def page_dict(items: Sequence[Any], page: int, page_size: int, total: int) -> dict[str, Any]:
    return {
        "items": list(items),
        "page": page,
        "page_size": page_size,
        "total": total,
        "has_more": page * page_size < total,
    }


def paginate_select(db: Session, stmt: Any, page: int = 1, page_size: int = 10) -> tuple[list[Any], int, int, int]:
    page = clamp_page(page)
    page_size = clamp_page_size(page_size)
    total = db.scalar(select(func.count()).select_from(stmt.subquery())) or 0
    rows = db.scalars(stmt.offset((page - 1) * page_size).limit(page_size)).all()
    return rows, page, page_size, total
