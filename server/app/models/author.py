"""
作者模型
"""

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class Author(Base):
    """作者表（诗人）"""

    __tablename__ = "authors"

    id = Column(BigInteger, primary_key=True, index=True, comment="作者ID")
    name = Column(String(50), nullable=False, index=True, comment="姓名")
    dynasty = Column(String(50), nullable=True, index=True, comment="朝代")
    intro = Column(Text, nullable=True, comment="简介")
    avatar = Column(String(500), nullable=True, comment="头像")
    birth_year = Column(Integer, nullable=True, comment="出生年份")
    death_year = Column(Integer, nullable=True, comment="逝世年份")

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
    poetries = relationship("Poetry", back_populates="author")

    def __repr__(self):
        return f"<Author {self.id} {self.name}>"
