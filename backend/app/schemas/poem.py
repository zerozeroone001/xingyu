from __future__ import annotations

from pydantic import BaseModel


class PoemQuery(BaseModel):
    page: int = 1
    page_size: int = 10
    keyword: str | None = None
    author: str | None = None
    dynasty: str | None = None
