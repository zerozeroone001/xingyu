"""
评论相关Schema
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict


class CommentBase(BaseModel):
    """评论基础Schema"""
    content: str = Field(..., min_length=1, max_length=2000, description="评论内容")


class CommentCreate(CommentBase):
    """创建评论"""
    target_type: str = Field(..., pattern="^(poetry|post)$", description="目标类型")
    target_id: int = Field(..., gt=0, description="目标ID")
    parent_id: Optional[int] = Field(None, description="父评论ID（二级评论）")


class CommentUpdate(BaseModel):
    """更新评论"""
    content: str = Field(..., min_length=1, max_length=2000, description="评论内容")


class UserSimple(BaseModel):
    """用户简化信息"""
    id: int
    nickname: str
    avatar: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class CommentResponse(CommentBase):
    """评论响应"""
    id: int
    user_id: int
    target_type: str
    target_id: int
    parent_id: Optional[int] = None
    like_count: int = 0
    reply_count: int = 0
    status: int
    created_at: datetime
    updated_at: datetime

    # 关联用户信息
    user: Optional[UserSimple] = None

    model_config = ConfigDict(from_attributes=True)


class CommentWithReplies(CommentResponse):
    """带回复的评论"""
    replies: List["CommentResponse"] = []

    model_config = ConfigDict(from_attributes=True)


class CommentQuery(BaseModel):
    """评论查询参数"""
    target_type: str = Field(..., pattern="^(poetry|post)$", description="目标类型")
    target_id: int = Field(..., gt=0, description="目标ID")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
    sort_by: str = Field("created_at", description="排序字段")
    order: str = Field("desc", pattern="^(asc|desc)$", description="排序方式")
