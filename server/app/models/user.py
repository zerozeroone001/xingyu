"""
用户模型
"""

from datetime import datetime
from sqlalchemy import Column, BigInteger, String, Integer, SmallInteger, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.core.database import Base


class User(Base):
    """用户表"""

    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, index=True, comment="用户ID")
    openid = Column(String(100), unique=True, nullable=True, comment="微信openid")
    unionid = Column(String(100), nullable=True, comment="微信unionid")
    username = Column(String(50), unique=True, nullable=True, index=True, comment="用户名")
    password = Column(String(255), nullable=True, comment="密码(bcrypt加密)")
    nickname = Column(String(50), nullable=False, comment="昵称")
    avatar = Column(String(500), nullable=True, comment="头像URL")
    phone = Column(String(20), nullable=True, index=True, comment="手机号")
    gender = Column(SmallInteger, default=0, comment="性别:0未知,1男,2女")
    intro = Column(String(500), nullable=True, comment="个人简介")
    level = Column(Integer, default=1, comment="用户等级")
    exp = Column(Integer, default=0, comment="经验值")
    status = Column(SmallInteger, default=1, index=True, comment="状态:1正常,2封禁")

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
    last_login_at = Column(DateTime, nullable=True, comment="最后登录时间")

    # 关系
    liked_poetries = relationship("UserPoetryLike", back_populates="user", cascade="all, delete-orphan")
    collected_poetries = relationship("UserPoetryCollection", back_populates="user", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<User {self.id} {self.nickname}>"
