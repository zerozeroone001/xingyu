"""
用户相关API
"""

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/users")


@router.get("/me", response_model=ResponseModel[UserResponse])
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
):
    """
    获取当前用户信息
    """
    return ResponseModel(
        code=0,
        message="success",
        data=UserResponse.model_validate(current_user),
    )


@router.put("/me", response_model=ResponseModel[UserResponse])
async def update_current_user(
    user_update: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    更新当前用户信息

    - **nickname**: 昵称
    - **avatar**: 头像URL
    - **gender**: 性别
    - **intro**: 个人简介
    """
    # 更新用户信息
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(current_user, field, value)

    await db.commit()
    await db.refresh(current_user)

    return ResponseModel(
        code=0,
        message="更新成功",
        data=UserResponse.model_validate(current_user),
    )


@router.get("/{user_id}", response_model=ResponseModel[UserResponse])
async def get_user_by_id(
    user_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    根据ID获取用户信息

    - **user_id**: 用户ID
    """
    from sqlalchemy import select

    result = await db.execute(
        select(User).where(User.id == user_id, User.status == 1)
    )
    user = result.scalar_one_or_none()

    if not user:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )

    return ResponseModel(
        code=0,
        message="success",
        data=UserResponse.model_validate(user),
    )
