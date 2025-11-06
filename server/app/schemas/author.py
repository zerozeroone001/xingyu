"""
作者相关Schema
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class AuthorBase(BaseModel):
    """作者基础Schema"""

    name: str = Field(..., min_length=1, max_length=50, description="姓名")
    dynasty: Optional[str] = Field(None, max_length=50, description="朝代")
    intro: Optional[str] = Field(None, description="简介")
    avatar: Optional[str] = Field(None, max_length=500, description="头像")
    birth_year: Optional[int] = Field(None, description="出生年份")
    death_year: Optional[int] = Field(None, description="逝世年份")


class AuthorCreate(AuthorBase):
    """创建作者Schema"""
    pass


class AuthorUpdate(BaseModel):
    """更新作者Schema"""

    name: Optional[str] = Field(None, min_length=1, max_length=50, description="姓名")
    dynasty: Optional[str] = Field(None, max_length=50, description="朝代")
    intro: Optional[str] = Field(None, description="简介")
    avatar: Optional[str] = Field(None, max_length=500, description="头像")
    birth_year: Optional[int] = Field(None, description="出生年份")
    death_year: Optional[int] = Field(None, description="逝世年份")


class AuthorResponse(AuthorBase):
    """作者响应Schema"""

    id: int = Field(..., description="作者ID")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "李白",
                "dynasty": "唐代",
                "intro": "字太白，号青莲居士...",
                "birth_year": 701,
                "death_year": 762,
                "created_at": "2024-01-01T00:00:00"
            }
        }


class AuthorSimple(BaseModel):
    """作者简化Schema（用于诗词详情中）"""

    id: int = Field(..., description="作者ID")
    name: str = Field(..., description="姓名")
    dynasty: Optional[str] = Field(None, description="朝代")

    class Config:
        from_attributes = True
