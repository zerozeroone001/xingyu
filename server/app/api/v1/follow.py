"""
关注相关API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.follow_service import FollowService
from app.schemas.follow import UserBasic, FollowStats
from app.schemas.response import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/follow")


@router.post("/{user_id}", response_model=ResponseModel[dict])
async def follow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    关注用户

    需要登录

    - **user_id**: 被关注用户ID
    """
    service = FollowService(db)
    success = await service.follow_user(current_user.id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无法关注该用户（可能已关注或无法关注自己）",
        )

    return ResponseModel(
        code=200,
        msg="关注成功",
        data={"following": True},
    )


@router.delete("/{user_id}", response_model=ResponseModel[dict])
async def unfollow_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    取消关注用户

    需要登录

    - **user_id**: 被关注用户ID
    """
    service = FollowService(db)
    success = await service.unfollow_user(current_user.id, user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未关注该用户",
        )

    return ResponseModel(
        code=200,
        msg="取消关注成功",
        data={"following": False},
    )


@router.get("/{user_id}/check", response_model=ResponseModel[dict])
async def check_following(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    检查是否已关注用户

    需要登录

    - **user_id**: 用户ID
    """
    service = FollowService(db)
    is_following = await service.check_following(current_user.id, user_id)

    return ResponseModel(
        code=200,
        msg="success",
        data={"is_following": is_following},
    )


@router.get("/{user_id}/stats", response_model=ResponseModel[FollowStats])
async def get_follow_stats(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取用户关注统计

    需要登录

    - **user_id**: 用户ID
    """
    service = FollowService(db)

    # 获取关注数和粉丝数
    following_count = await service.get_following_count(user_id)
    followers_count = await service.get_followers_count(user_id)

    # 检查当前用户与目标用户的关注关系
    is_following = await service.check_following(current_user.id, user_id)
    is_followed = await service.check_following(user_id, current_user.id)

    return ResponseModel(
        code=200,
        msg="success",
        data=FollowStats(
            following_count=following_count,
            followers_count=followers_count,
            is_following=is_following,
            is_followed=is_followed,
        ),
    )


@router.get("/following/list", response_model=ResponseModel[PaginatedResponse[UserBasic]])
async def get_following_list(
    user_id: int = Query(..., description="用户ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户的关注列表

    - **user_id**: 用户ID
    - **page**: 页码
    - **page_size**: 每页数量
    """
    service = FollowService(db)
    users, total = await service.get_following_list(user_id, page, page_size)

    # 转换为Basic格式
    items = [UserBasic.model_validate(u) for u in users]

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return ResponseModel(
        code=200,
        msg="success",
        data=PaginatedResponse(
            list=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
    )


@router.get("/followers/list", response_model=ResponseModel[PaginatedResponse[UserBasic]])
async def get_followers_list(
    user_id: int = Query(..., description="用户ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取用户的粉丝列表

    - **user_id**: 用户ID
    - **page**: 页码
    - **page_size**: 每页数量
    """
    service = FollowService(db)
    users, total = await service.get_followers_list(user_id, page, page_size)

    # 转换为Basic格式
    items = [UserBasic.model_validate(u) for u in users]

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return ResponseModel(
        code=200,
        msg="success",
        data=PaginatedResponse(
            list=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
    )


@router.get("/friends/list", response_model=ResponseModel[PaginatedResponse[UserBasic]])
async def get_friends_list(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取互相关注列表（好友列表）

    需要登录

    - **page**: 页码
    - **page_size**: 每页数量
    """
    service = FollowService(db)
    users, total = await service.get_mutual_following(current_user.id, page, page_size)

    # 转换为Basic格式
    items = [UserBasic.model_validate(u) for u in users]

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return ResponseModel(
        code=200,
        msg="success",
        data=PaginatedResponse(
            list=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
    )
