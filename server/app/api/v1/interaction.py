"""
用户诗词交互API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.interaction_service import PoetryInteractionService
from app.schemas.poetry import PoetryDetail
from app.schemas.response import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/interactions")


# ============ 点赞相关 ============

@router.post("/like/{poetry_id}", response_model=ResponseModel[dict])
async def like_poetry(
    poetry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    点赞诗词

    需要登录
    """
    service = PoetryInteractionService(db)
    success = await service.like_poetry(current_user.id, poetry_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经点赞过该诗词",
        )

    return ResponseModel(
        code=0,
        message="点赞成功",
        data={"liked": True},
    )


@router.delete("/like/{poetry_id}", response_model=ResponseModel[dict])
async def unlike_poetry(
    poetry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    取消点赞诗词

    需要登录
    """
    service = PoetryInteractionService(db)
    success = await service.unlike_poetry(current_user.id, poetry_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未点赞过该诗词",
        )

    return ResponseModel(
        code=0,
        message="取消点赞成功",
        data={"liked": False},
    )


@router.get("/like/{poetry_id}/check", response_model=ResponseModel[dict])
async def check_poetry_liked(
    poetry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    检查是否已点赞诗词

    需要登录
    """
    service = PoetryInteractionService(db)
    liked = await service.check_liked(current_user.id, poetry_id)

    return ResponseModel(
        code=0,
        message="success",
        data={"liked": liked},
    )


@router.get("/likes", response_model=ResponseModel[PaginatedResponse[PoetryDetail]])
async def get_liked_poetries(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取用户点赞的诗词列表

    需要登录
    """
    service = PoetryInteractionService(db)
    poetries, total = await service.get_user_liked_poetries(
        current_user.id, page, page_size
    )

    # 转换为Detail格式
    items = [PoetryDetail.model_validate(p) for p in poetries]

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return ResponseModel(
        code=0,
        message="success",
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
    )


# ============ 收藏相关 ============

@router.post("/collect/{poetry_id}", response_model=ResponseModel[dict])
async def collect_poetry(
    poetry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    收藏诗词

    需要登录
    """
    service = PoetryInteractionService(db)
    success = await service.collect_poetry(current_user.id, poetry_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="已经收藏过该诗词",
        )

    return ResponseModel(
        code=0,
        message="收藏成功",
        data={"collected": True},
    )


@router.delete("/collect/{poetry_id}", response_model=ResponseModel[dict])
async def uncollect_poetry(
    poetry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    取消收藏诗词

    需要登录
    """
    service = PoetryInteractionService(db)
    success = await service.uncollect_poetry(current_user.id, poetry_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="未收藏过该诗词",
        )

    return ResponseModel(
        code=0,
        message="取消收藏成功",
        data={"collected": False},
    )


@router.get("/collect/{poetry_id}/check", response_model=ResponseModel[dict])
async def check_poetry_collected(
    poetry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    检查是否已收藏诗词

    需要登录
    """
    service = PoetryInteractionService(db)
    collected = await service.check_collected(current_user.id, poetry_id)

    return ResponseModel(
        code=0,
        message="success",
        data={"collected": collected},
    )


@router.get("/collections", response_model=ResponseModel[PaginatedResponse[PoetryDetail]])
async def get_collected_poetries(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取用户收藏的诗词列表

    需要登录
    """
    service = PoetryInteractionService(db)
    poetries, total = await service.get_user_collected_poetries(
        current_user.id, page, page_size
    )

    # 转换为Detail格式
    items = [PoetryDetail.model_validate(p) for p in poetries]

    # 计算总页数
    total_pages = (total + page_size - 1) // page_size

    return ResponseModel(
        code=0,
        message="success",
        data=PaginatedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
            total_pages=total_pages,
        ),
    )
