"""
用户诗词交互模型
"""

from datetime import datetime
from sqlalchemy import (
    Column,
    BigInteger,
    ForeignKey,
    DateTime,
    Index,
    text,
)
from sqlalchemy.orm import relationship

from app.core.database import Base


class UserPoetryLike(Base):
    """用户点赞诗词关联表"""

    __tablename__ = "user_poetry_likes"

    id = Column(BigInteger, primary_key=True, index=True, comment="ID")
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="用户ID",
    )
    poetry_id = Column(
        BigInteger,
        ForeignKey("poetries.id", ondelete="CASCADE"),
        nullable=False,
        comment="诗词ID",
    )
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )

    # 关系
    user = relationship("User", back_populates="liked_poetries")
    poetry = relationship("Poetry", back_populates="liked_by_users")

    __table_args__ = (
        Index("ix_user_poetry_like_user_id", "user_id"),
        Index("ix_user_poetry_like_poetry_id", "poetry_id"),
        Index("ix_user_poetry_like_unique", "user_id", "poetry_id", unique=True),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci", "mysql_engine": "InnoDB"},
    )

    def __repr__(self):
        return f"<UserPoetryLike(user_id={self.user_id}, poetry_id={self.poetry_id})>"


class UserPoetryCollection(Base):
    """用户收藏诗词关联表"""

    __tablename__ = "user_poetry_collections"

    id = Column(BigInteger, primary_key=True, index=True, comment="ID")
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        comment="用户ID",
    )
    poetry_id = Column(
        BigInteger,
        ForeignKey("poetries.id", ondelete="CASCADE"),
        nullable=False,
        comment="诗词ID",
    )
    created_at = Column(
        DateTime,
        server_default=text("CURRENT_TIMESTAMP"),
        comment="创建时间",
    )

    # 关系
    user = relationship("User", back_populates="collected_poetries")
    poetry = relationship("Poetry", back_populates="collected_by_users")

    __table_args__ = (
        Index("ix_user_poetry_collection_user_id", "user_id"),
        Index("ix_user_poetry_collection_poetry_id", "poetry_id"),
        Index("ix_user_poetry_collection_unique", "user_id", "poetry_id", unique=True),
        {"mysql_charset": "utf8mb4", "mysql_collate": "utf8mb4_unicode_ci", "mysql_engine": "InnoDB"},
    )

    def __repr__(self):
        return f"<UserPoetryCollection(user_id={self.user_id}, poetry_id={self.poetry_id})>"
