from __future__ import annotations

from pydantic import BaseModel


class UserUpdate(BaseModel):
    nickname: str | None = None
    avatar_url: str | None = None
    avatarText: str | None = None
    avatar_text: str | None = None
    title: str | None = None
    gender: str | None = None
    city: str | None = None
    bio: str | None = None
