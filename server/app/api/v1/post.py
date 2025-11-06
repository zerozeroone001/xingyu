"""
广场内容相关API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, get_optional_current_user
from app.models.user import User
from app.services.post_service import PostService
from app.schemas.post import (
    PostCreate,
    PostUpdate,
    PostResponse,
)
from app.schemas.response import ResponseModel, PagedResponse

router = APIRouter(prefix="/posts")


@router.get("", response_model=ResponseModel[PagedResponse[PostResponse]])
async def get_posts(
    type_: str = Query(None, alias="type", pattern="^(original|share)$", description="类型"),
    user_id: int = Query(None, description="用户ID"),
    tag: str = Query(None, description="标签"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    order_by: str = Query(
        "created_at",
        pattern="^(created_at|like_count|view_count)$",
        description="排序字段",
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    获取广场内容列表

    - **type**: 类型筛选（original/share）
    - **user_id**: 用户ID筛选
    - **tag**: 标签筛选
    - **page**: 页码
    - **page_size**: 每页数量（1-100）
    - **order_by**: 排序字段（created_at/like_count/view_count）
    """
    service = PostService(db)
    posts, total = await service.get_list(
        type_=type_,
        user_id=user_id,
        tag=tag,
        status=1,
        page=page,
        page_size=page_size,
        order_by=order_by,
    )

    items = [PostResponse.model_validate(p) for p in posts]

    return ResponseModel(
        code=0,
        message="success",
        data=PagedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        ),
    )


@router.get("/following", response_model=ResponseModel[PagedResponse[PostResponse]])
async def get_following_posts(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取关注用户的动态（需要登录）

    - **page**: 页码
    - **page_size**: 每页数量（1-100）
    """
    service = PostService(db)
    posts, total = await service.get_following_posts(
        user_id=current_user.id, page=page, page_size=page_size
    )

    items = [PostResponse.model_validate(p) for p in posts]

    return ResponseModel(
        code=0,
        message="success",
        data=PagedResponse(
            items=items,
            total=total,
            page=page,
            page_size=page_size,
        ),
    )


@router.get("/{post_id}", response_model=ResponseModel[PostResponse])
async def get_post_detail(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_optional_current_user),
):
    """
    获取广场内容详情

    - **post_id**: 内容ID
    """
    service = PostService(db)
    post = await service.get_by_id(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="内容不存在")

    if post.status != 1:
        raise HTTPException(status_code=404, detail="内容已删除或不可见")

    # 增加浏览数
    await service.increment_view_count(post_id)

    return ResponseModel(
        code=0,
        message="success",
        data=PostResponse.model_validate(post),
    )


@router.post("", response_model=ResponseModel[PostResponse])
async def create_post(
    post_data: PostCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建广场内容（需要登录）

    - **content**: 内容（1-5000字）
    - **images**: 图片URLs（可选）
    - **tags**: 标签（可选）
    - **poetry_id**: 关联诗词ID（分享时使用）
    - **type**: 类型（original/share，默认original）
    """
    service = PostService(db)

    try:
        post = await service.create(user_id=current_user.id, post_data=post_data)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    return ResponseModel(
        code=0,
        message="发布成功",
        data=PostResponse.model_validate(post),
    )


@router.put("/{post_id}", response_model=ResponseModel[PostResponse])
async def update_post(
    post_id: int,
    post_data: PostUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新广场内容（需要登录）

    - **post_id**: 内容ID
    - **content**: 内容（可选）
    - **images**: 图片URLs（可选）
    - **tags**: 标签（可选）
    - **status**: 状态（可选）
    """
    service = PostService(db)

    try:
        post = await service.update(
            post_id=post_id, user_id=current_user.id, post_data=post_data
        )
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    if not post:
        raise HTTPException(status_code=404, detail="内容不存在")

    return ResponseModel(
        code=0,
        message="更新成功",
        data=PostResponse.model_validate(post),
    )


@router.delete("/{post_id}", response_model=ResponseModel[None])
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除广场内容（需要登录）

    - **post_id**: 内容ID
    """
    service = PostService(db)

    try:
        success = await service.delete(post_id=post_id, user_id=current_user.id)
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))

    if not success:
        raise HTTPException(status_code=404, detail="内容不存在")

    return ResponseModel(
        code=0,
        message="删除成功",
        data=None,
    )
