"""
消息相关Schema
"""

from typing import Optional, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict


class UserSimple(BaseModel):
    """用户简要信息"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    nickname: str
    avatar: Optional[str] = None


class MessageBase(BaseModel):
    """消息基础Schema"""
    type: str = Field(..., description="消息类型")
    title: str = Field(..., min_length=1, max_length=100, description="消息标题")
    content: Optional[str] = Field(None, description="消息内容")
    data: Optional[Dict[str, Any]] = Field(None, description="关联数据")
    target_type: Optional[str] = Field(None, description="目标类型")
    target_id: Optional[int] = Field(None, description="目标ID")


class MessageCreate(MessageBase):
    """创建消息"""
    user_id: int = Field(..., description="接收用户ID")
    from_user_id: Optional[int] = Field(None, description="发送者ID")


class MessageResponse(BaseModel):
    """消息响应"""
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    type: str
    title: str
    content: Optional[str] = None
    data: Optional[Dict[str, Any]] = None
    from_user_id: Optional[int] = None
    target_type: Optional[str] = None
    target_id: Optional[int] = None
    is_read: int
    created_at: datetime
    read_at: Optional[datetime] = None

    # 关联信息
    from_user: Optional[UserSimple] = None


class MessageStats(BaseModel):
    """消息统计"""
    total: int = Field(..., description="总消息数")
    unread: int = Field(..., description="未读消息数")
    system: int = Field(0, description="系统消息数")
    like: int = Field(0, description="点赞消息数")
    comment: int = Field(0, description="评论消息数")
    follow: int = Field(0, description="关注消息数")
    collect: int = Field(0, description="收藏消息数")


class MessageQuery(BaseModel):
    """消息查询参数"""
    type: Optional[str] = Field(None, description="消息类型筛选")
    is_read: Optional[int] = Field(None, ge=0, le=1, description="读取状态")
    page: int = Field(1, ge=1, description="页码")
    page_size: int = Field(20, ge=1, le=100, description="每页数量")
