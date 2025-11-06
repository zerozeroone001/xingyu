"""
消息模型
"""

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, SmallInteger, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Message(Base):
    """消息表"""

    __tablename__ = "messages"

    id = Column(BigInteger, primary_key=True, index=True, comment="消息ID")
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="接收用户ID"
    )

    # 消息类型：system系统消息, like点赞, comment评论, follow关注, collect收藏
    type = Column(
        String(20),
        nullable=False,
        index=True,
        comment="消息类型"
    )

    title = Column(String(100), nullable=False, comment="消息标题")
    content = Column(Text, nullable=True, comment="消息内容")

    # 关联数据（JSON格式存储相关信息）
    # 例如：{"poetry_id": 123, "comment_id": 456, "from_user_id": 789}
    data = Column(JSON, nullable=True, comment="关联数据")

    # 发送者ID（互动消息使用）
    from_user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="发送者ID"
    )

    # 目标类型和ID（用于关联诗词、动态等）
    target_type = Column(String(20), nullable=True, comment="目标类型:poetry,post,comment")
    target_id = Column(BigInteger, nullable=True, comment="目标ID")

    # 读取状态：0未读，1已读
    is_read = Column(SmallInteger, default=0, index=True, comment="是否已读:0未读,1已读")

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
        comment="创建时间"
    )
    read_at = Column(DateTime, nullable=True, comment="阅读时间")

    # 关系
    user = relationship("User", foreign_keys=[user_id])
    from_user = relationship("User", foreign_keys=[from_user_id])

    def __repr__(self):
        return f"<Message {self.id} to User {self.user_id}>"
