"""
关注相关Schema
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class UserBasic(BaseModel):
    """用户基础信息"""
    id: int
    nickname: str
    avatar: Optional[str] = None
    intro: Optional[str] = None
    level: int = 1

    model_config = ConfigDict(from_attributes=True)


class FollowStats(BaseModel):
    """关注统计"""
    following_count: int
    followers_count: int
    is_following: bool = False  # 当前用户是否关注了该用户
    is_followed: bool = False  # 该用户是否关注了当前用户
