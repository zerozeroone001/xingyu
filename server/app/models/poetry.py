"""
诗词模型
"""

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, SmallInteger, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Poetry(Base):
    """诗词表"""

    __tablename__ = "poetries"

    id = Column(BigInteger, primary_key=True, index=True, comment="诗词ID")
    title = Column(String(100), nullable=False, index=True, comment="标题")
    content = Column(Text, nullable=False, comment="内容")
    author_id = Column(
        BigInteger,
        ForeignKey("authors.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="作者ID"
    )
    dynasty = Column(String(50), nullable=True, index=True, comment="朝代")
    type = Column(String(50), nullable=True, index=True, comment="类型:绝句,律诗,词等")
    tags = Column(JSON, nullable=True, comment="标签")
    translation = Column(Text, nullable=True, comment="翻译")
    annotation = Column(Text, nullable=True, comment="注释")
    appreciation = Column(Text, nullable=True, comment="赏析")
    background = Column(Text, nullable=True, comment="创作背景")

    # 统计字段
    read_count = Column(Integer, default=0, comment="阅读数")
    like_count = Column(Integer, default=0, comment="点赞数")
    comment_count = Column(Integer, default=0, comment="评论数")
    collect_count = Column(Integer, default=0, comment="收藏数")

    status = Column(
        SmallInteger,
        default=1,
        index=True,
        comment="状态:1已发布,2草稿,3已删除"
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
    author = relationship("Author", back_populates="poetries")
    liked_by_users = relationship("UserPoetryLike", back_populates="poetry", cascade="all, delete-orphan")
    collected_by_users = relationship("UserPoetryCollection", back_populates="poetry", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Poetry {self.id} {self.title}>"
