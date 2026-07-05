from __future__ import annotations

from pydantic import BaseModel


class WxLoginRequest(BaseModel):
    code: str = ""
    profile: dict = {}


class LoginResponse(BaseModel):
    token: str
    user: dict
