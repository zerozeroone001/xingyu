"""
广场内容模型
"""

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, SmallInteger, Text, DateTime, ForeignKey, JSON
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Post(Base):
    """广场内容表"""

    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True, index=True, comment="内容ID")
    user_id = Column(
        BigInteger,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
        comment="用户ID"
    )
    content = Column(Text, nullable=False, comment="内容")
    images = Column(JSON, nullable=True, comment="图片URLs（JSON数组）")
    tags = Column(JSON, nullable=True, comment="标签（JSON数组）")

    # 关联诗词（分享诗词时使用）
    poetry_id = Column(
        BigInteger,
        ForeignKey("poetries.id", ondelete="SET NULL"),
        nullable=True,
        index=True,
        comment="关联诗词ID"
    )

    type = Column(
        String(20),
        default="original",
        index=True,
        comment="类型:original原创,share分享"
    )

    # 统计字段
    like_count = Column(Integer, default=0, comment="点赞数")
    comment_count = Column(Integer, default=0, comment="评论数")
    collect_count = Column(Integer, default=0, comment="收藏数")
    view_count = Column(Integer, default=0, comment="浏览数")

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
    user = relationship("User", back_populates="posts")
    poetry = relationship("Poetry")

    def __repr__(self):
        return f"<Post {self.id} by User {self.user_id}>"
