"""
广场内容相关Schema
"""

from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class UserSimple(BaseModel):
    """用户简要信息"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    nickname: str
    avatar: Optional[str] = None
    level: Optional[int] = 1


class PoetrySimple(BaseModel):
    """诗词简要信息"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    author_name: Optional[str] = None
    dynasty: Optional[str] = None


class PostBase(BaseModel):
    """广场内容基础Schema"""
    content: str = Field(..., min_length=1, max_length=5000, description="内容")
    images: Optional[List[str]] = Field(None, description="图片URLs")
    tags: Optional[List[str]] = Field(None, description="标签")
    poetry_id: Optional[int] = Field(None, description="关联诗词ID")
    type: str = Field("original", pattern="^(original|share)$", description="类型")


class PostCreate(PostBase):
    """创建广场内容"""
    pass


class PostUpdate(BaseModel):
    """更新广场内容"""
    content: Optional[str] = Field(None, min_length=1, max_length=5000, description="内容")
    images: Optional[List[str]] = Field(None, description="图片URLs")
    tags: Optional[List[str]] = Field(None, description="标签")
    status: Optional[int] = Field(None, ge=1, le=3, description="状态")


class PostResponse(BaseModel):
    """广场内容响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    content: str
    images: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    poetry_id: Optional[int] = None
    type: str
    like_count: int = 0
    comment_count: int = 0
    collect_count: int = 0
    view_count: int = 0
    status: int
    created_at: datetime
    updated_at: datetime

    # 关联信息
    user: Optional[UserSimple] = None
    poetry: Optional[PoetrySimple] = None

    # 当前用户交互状态
    is_liked: Optional[bool] = False
    is_collected: Optional[bool] = False


class PostQuery(BaseModel):
    """广场内容查询参数"""
    type: Optional[str] = Field(None, pattern="^(original|share)$", description="类型")
    user_id: Optional[int] = Field(None, description="用户ID")
    tag: Optional[str] = Field(None, description="标签")
    status: Optional[int] = Field(None, ge=1, le=3, description="状态")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    order_by: str = Field("created_at", pattern="^(created_at|like_count|view_count)$", description="排序字段")
