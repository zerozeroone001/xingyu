from __future__ import annotations

from pydantic import BaseModel, Field


class SquareTopicCreate(BaseModel):
    content: str = Field(min_length=1, max_length=2000)
    title: str | None = None
    badge: str | None = None
    tags: list[str] = []
    images: list[str] = []


class SquareCommentCreate(BaseModel):
    content: str = Field(min_length=1, max_length=1000)
