from __future__ import annotations

from pydantic import BaseModel, Field


class AdminLoginRequest(BaseModel):
    username: str
    password: str


class PoemAdminPayload(BaseModel):
    title: str = Field(min_length=1, max_length=120)
    dynasty: str = Field(min_length=1, max_length=40)
    author: str = Field(min_length=1, max_length=80)
    content: str = Field(min_length=1)
    recommend_sentence: str = ""
    tags: list[str] = Field(default_factory=list)
    category_ids: list[int] = Field(default_factory=list)
    like_count: int = 0
    favorite_count: int = 0
    share_count: int = 0


class CategoryAdminPayload(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    type: str = Field(min_length=1, max_length=40)
    sort_order: int = 0


class UserAdminPayload(BaseModel):
    nickname: str | None = Field(default=None, max_length=80)
    avatar_text: str | None = Field(default=None, max_length=8)
    title: str | None = Field(default=None, max_length=80)
    level: int | None = None
    gender: str | None = Field(default=None, max_length=20)
    city: str | None = Field(default=None, max_length=80)
    bio: str | None = None


class SquareTopicAdminPayload(BaseModel):
    title: str | None = Field(default=None, max_length=160)
    content: str | None = None
    badge: str | None = Field(default=None, max_length=40)
    tags: list[str] | None = None
    images: list[str] | None = None


class FeedbackAdminPayload(BaseModel):
    status: str = Field(min_length=1, max_length=40)


class FeihualingRoomAdminPayload(BaseModel):
    title: str | None = Field(default=None, max_length=120)
    keyword: str | None = Field(default=None, max_length=20)
    can_watch: bool | None = None
    player_count: int | None = None
    max_players: int | None = None
    round_text: str | None = Field(default=None, max_length=80)
