"""
评论模型
"""

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, SmallInteger, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Comment(Base):
    """评论表"""

    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, index=True, comment="评论ID")
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    target_type = Column(
        String(20),
        nullable=False,
        index=True,
        comment="目标类型:poetry,post"
    )
    target_id = Column(
        BigInteger,
        nullable=False,
        index=True,
        comment="目标ID"
    )
    parent_id = Column(
        BigInteger,
        ForeignKey("comments.id", ondelete="CASCADE"),
        nullable=True,
        index=True,
        comment="父评论ID（二级评论）"
    )
    content = Column(Text, nullable=False, comment="评论内容")
    like_count = Column(Integer, default=0, comment="点赞数")
    reply_count = Column(Integer, default=0, comment="回复数")
    status = Column(
        SmallInteger,
        default=1,
        index=True,
        comment="状态:1正常,2已删除"
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
        comment="创建时间"
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default=func.now(),
        server_onupdate=func.now(),
        comment="更新时间"
    )

    # 关系
    user = relationship("User", back_populates="comments")
    parent = relationship("Comment", remote_side=[id], back_populates="replies")
    replies = relationship("Comment", back_populates="parent", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Comment {self.id} by User {self.user_id}>"
