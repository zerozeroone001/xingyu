from __future__ import annotations

from pydantic import BaseModel, Field


class FeihualingCheckRequest(BaseModel):
    keyword: str = Field(min_length=1, max_length=10)
    answer: str = Field(min_length=1, max_length=300)


class FeihualingRecordCreate(BaseModel):
    keyword: str
    answer: str
    is_correct: bool = False
    score: int = 0
    source: dict | None = None


class FeihualingRoomCreate(BaseModel):
    title: str | None = None
    keyword: str = Field(min_length=1, max_length=10)
    canWatch: bool | None = None
    can_watch: bool | None = None
    maxPlayers: int | None = None
    max_players: int | None = None
