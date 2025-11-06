"""
关注模型
"""

from datetime import datetime
from sqlalchemy import Column, BigInteger, DateTime, ForeignKey, Index, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Follow(Base):
    """关注表"""

    __tablename__ = "follows"

    id = Column(BigInteger, primary_key=True, index=True, comment="ID")
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="关注者ID"
    )
    follow_user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="被关注者ID"
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        server_default=func.now(),
        comment="创建时间"
    )

    # 关系
    follower = relationship("User", foreign_keys=[user_id], back_populates="following")
    following = relationship("User", foreign_keys=[follow_user_id], back_populates="followers")

    __table_args__ = (
        UniqueConstraint("user_id", "follow_user_id", name="uk_user_follow"),
        Index("ix_follow_user_id", "follow_user_id"),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci", "mysql_engine": "InnoDB"},
    )

    def __repr__(self):
        return f"<Follow user_id={self.user_id} follow_user_id={self.follow_user_id}>"
