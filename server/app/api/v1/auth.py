"""
认证相关API
"""

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.core.database import get_db
from app.core.security import (
    verify_password,
    get_password_hash,
    create_access_token,
    create_refresh_token,
)
from app.models.user import User
from app.schemas.user import (
    UserRegister,
    UserLogin,
    WechatLogin,
    TokenResponse,
    UserResponse,
)
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/auth")


@router.post("/register", response_model=ResponseModel[TokenResponse])
async def register(
    user_data: UserRegister,
    db: AsyncSession = Depends(get_db),
):
    """
    用户注册

    - **username**: 用户名(3-50字符,只能包含字母和数字)
    - **password**: 密码(最少6字符)
    - **nickname**: 昵称
    """
    # 检查用户名是否已存在
    result = await db.execute(
        select(User).where(User.username == user_data.username)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="用户名已存在",
        )

    # 创建新用户
    hashed_password = get_password_hash(user_data.password)
    new_user = User(
        username=user_data.username,
        password=hashed_password,
        nickname=user_data.nickname,
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    # 生成Token
    access_token = create_access_token({"user_id": new_user.id})
    refresh_token = create_refresh_token({"user_id": new_user.id})

    # 返回响应
    return ResponseModel(
        code=0,
        message="注册成功",
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(new_user),
        ),
    )


@router.post("/login", response_model=ResponseModel[TokenResponse])
async def login(
    login_data: UserLogin,
    db: AsyncSession = Depends(get_db),
):
    """
    用户登录

    - **username**: 用户名
    - **password**: 密码
    """
    # 查询用户
    result = await db.execute(
        select(User).where(User.username == login_data.username)
    )
    user = result.scalar_one_or_none()

    # 验证用户和密码
    if not user or not verify_password(login_data.password, user.password or ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户名或密码错误",
        )

    # 检查用户状态
    if user.status != 1:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="用户已被禁用",
        )

    # 更新最后登录时间
    user.last_login_at = datetime.utcnow()
    await db.commit()

    # 生成Token
    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})

    # 返回响应
    return ResponseModel(
        code=0,
        message="登录成功",
        data=TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
            user=UserResponse.model_validate(user),
        ),
    )


@router.post("/login/wechat", response_model=ResponseModel[TokenResponse])
async def wechat_login(
    wechat_data: WechatLogin,
    db: AsyncSession = Depends(get_db),
):
    """
    微信小程序登录

    - **code**: 微信登录code
    - **encrypted_data**: 加密数据(可选)
    - **iv**: 初始向量(可选)
    """
    # TODO: 调用微信API获取openid
    # 这里暂时模拟实现
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="微信登录功能开发中",
    )


@router.post("/refresh", response_model=ResponseModel[TokenResponse])
async def refresh_token(
    refresh_token: str,
    db: AsyncSession = Depends(get_db),
):
    """
    刷新Token

    - **refresh_token**: 刷新令牌
    """
    from app.core.security import decode_token

    # 解码刷新Token
    payload = decode_token(refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="无效的刷新令牌",
        )

    user_id = payload.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="令牌中缺少用户信息",
        )

    # 查询用户
    result = await db.execute(
        select(User).where(User.id == user_id, User.status == 1)
    )
    user = result.scalar_one_or_none()

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户不存在或已被禁用",
        )

    # 生成新Token
    new_access_token = create_access_token({"user_id": user.id})
    new_refresh_token = create_refresh_token({"user_id": user.id})

    return ResponseModel(
        code=0,
        message="刷新成功",
        data=TokenResponse(
            access_token=new_access_token,
            refresh_token=new_refresh_token,
            user=UserResponse.model_validate(user),
        ),
    )
