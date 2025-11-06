"""
用户相关Schema
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, field_validator


class UserBase(BaseModel):
    """用户基础Schema"""

    nickname: str = Field(..., min_length=1, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=500, description="头像URL")
    gender: int = Field(default=0, ge=0, le=2, description="性别:0未知,1男,2女")
    intro: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserRegister(BaseModel):
    """用户注册Schema"""

    username: str = Field(..., min_length=3, max_length=50, description="用户名")
    password: str = Field(..., min_length=6, max_length=50, description="密码")
    nickname: str = Field(..., min_length=1, max_length=50, description="昵称")

    @field_validator("username")
    @classmethod
    def validate_username(cls, v):
        """验证用户名格式"""
        if not v.isalnum():
            raise ValueError("用户名只能包含字母和数字")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "username": "zhangsan",
                "password": "password123",
                "nickname": "张三"
            }
        }


class UserLogin(BaseModel):
    """用户登录Schema"""

    username: str = Field(..., description="用户名")
    password: str = Field(..., description="密码")

    class Config:
        json_schema_extra = {
            "example": {
                "username": "zhangsan",
                "password": "password123"
            }
        }


class WechatLogin(BaseModel):
    """微信登录Schema"""

    code: str = Field(..., description="微信登录code")
    encrypted_data: Optional[str] = Field(None, description="加密数据")
    iv: Optional[str] = Field(None, description="加密算法的初始向量")

    class Config:
        json_schema_extra = {
            "example": {
                "code": "wx_code_from_wx_login",
                "encrypted_data": "encrypted_data",
                "iv": "iv"
            }
        }


class UserCreate(UserBase):
    """创建用户Schema"""

    username: Optional[str] = Field(None, max_length=50, description="用户名")
    password: Optional[str] = Field(None, max_length=255, description="密码")
    openid: Optional[str] = Field(None, max_length=100, description="微信openid")


class UserUpdate(BaseModel):
    """更新用户Schema"""

    nickname: Optional[str] = Field(None, min_length=1, max_length=50, description="昵称")
    avatar: Optional[str] = Field(None, max_length=500, description="头像URL")
    gender: Optional[int] = Field(None, ge=0, le=2, description="性别")
    intro: Optional[str] = Field(None, max_length=500, description="个人简介")


class UserResponse(UserBase):
    """用户响应Schema"""

    id: int = Field(..., description="用户ID")
    username: Optional[str] = Field(None, description="用户名")
    phone: Optional[str] = Field(None, description="手机号")
    level: int = Field(..., description="用户等级")
    exp: int = Field(..., description="经验值")
    status: int = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
    last_login_at: Optional[datetime] = Field(None, description="最后登录时间")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "username": "zhangsan",
                "nickname": "张三",
                "avatar": "https://example.com/avatar.jpg",
                "gender": 1,
                "phone": "13800138000",
                "level": 5,
                "exp": 1000,
                "status": 1,
                "created_at": "2024-01-01T00:00:00",
                "last_login_at": "2024-01-10T10:00:00"
            }
        }


class TokenResponse(BaseModel):
    """Token响应Schema"""

    access_token: str = Field(..., description="访问令牌")
    refresh_token: str = Field(..., description="刷新令牌")
    token_type: str = Field(default="bearer", description="令牌类型")
    user: UserResponse = Field(..., description="用户信息")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
                "user": {
                    "id": 1,
                    "username": "zhangsan",
                    "nickname": "张三"
                }
            }
        }
