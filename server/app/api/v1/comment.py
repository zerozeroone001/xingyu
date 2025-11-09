"""
评论相关API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.comment_service import CommentService
from app.schemas.comment import (
    CommentCreate,
    CommentUpdate,
    CommentResponse,
    CommentWithReplies,
)
from app.schemas.response import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/comments")


@router.get("/", response_model=ResponseModel[PaginatedResponse[CommentResponse]])
async def get_comments(
    target_type: str = Query(..., pattern="^(poetry|post)$", description="目标类型"),
    target_id: int = Query(..., gt=0, description="目标ID"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    sort_by: str = Query("created_at", description="排序字段"),
    order: str = Query("desc", pattern="^(asc|desc)$", description="排序方式"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取评论列表（仅一级评论）

    - **target_type**: 目标类型（poetry或post）
    - **target_id**: 目标ID
    - **page**: 页码
    - **page_size**: 每页数量
    - **sort_by**: 排序字段（created_at, like_count）
    - **order**: 排序方式（asc, desc）
    """
    service = CommentService(db)
    comments, total = await service.get_list(
        target_type=target_type,
        target_id=target_id,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        order=order,
    )

    # 转换为Response格式
    items = [CommentResponse.model_validate(c) for c in comments]

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


@router.get("/{comment_id}", response_model=ResponseModel[CommentResponse])
async def get_comment_detail(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取评论详情

    - **comment_id**: 评论ID
    """
    service = CommentService(db)
    comment = await service.get_by_id(comment_id)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在",
        )

    return ResponseModel(
        code=200,
        msg="success",
        data=CommentResponse.model_validate(comment),
    )


@router.get(
    "/{comment_id}/replies",
    response_model=ResponseModel[PaginatedResponse[CommentResponse]],
)
async def get_comment_replies(
    comment_id: int,
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(10, ge=1, le=50, description="每页数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取评论的回复列表（二级评论）

    - **comment_id**: 父评论ID
    - **page**: 页码
    - **page_size**: 每页数量
    """
    service = CommentService(db)

    # 检查父评论是否存在
    parent = await service.get_by_id(comment_id)
    if not parent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在",
        )

    replies, total = await service.get_replies(comment_id, page, page_size)

    # 转换为Response格式
    items = [CommentResponse.model_validate(r) for r in replies]

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


@router.post("/", response_model=ResponseModel[CommentResponse], status_code=status.HTTP_201_CREATED)
async def create_comment(
    comment_data: CommentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建评论

    需要登录

    - **target_type**: 目标类型（poetry或post）
    - **target_id**: 目标ID
    - **content**: 评论内容
    - **parent_id**: 父评论ID（可选，二级评论时填写）
    """
    service = CommentService(db)

    # 如果是二级评论，检查父评论是否存在
    if comment_data.parent_id:
        parent = await service.get_by_id(comment_data.parent_id)
        if not parent:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="父评论不存在",
            )

        # 二级评论必须与父评论的目标一致
        if (
            parent.target_type != comment_data.target_type
            or parent.target_id != comment_data.target_id
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="回复的评论目标不一致",
            )

    comment = await service.create(current_user.id, comment_data)

    return ResponseModel(
        code=200,
        msg="评论成功",
        data=CommentResponse.model_validate(comment),
    )


@router.put("/{comment_id}", response_model=ResponseModel[CommentResponse])
async def update_comment(
    comment_id: int,
    comment_data: CommentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新评论

    需要登录，只能更新自己的评论

    - **comment_id**: 评论ID
    - **content**: 评论内容
    """
    service = CommentService(db)
    comment = await service.update(comment_id, current_user.id, comment_data)

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在或无权限修改",
        )

    return ResponseModel(
        code=200,
        msg="更新成功",
        data=CommentResponse.model_validate(comment),
    )


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除评论

    需要登录，只能删除自己的评论

    - **comment_id**: 评论ID
    """
    service = CommentService(db)
    success = await service.delete(comment_id, current_user.id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在或无权限删除",
        )

    return None


@router.get("/user/my", response_model=ResponseModel[PaginatedResponse[CommentResponse]])
async def get_my_comments(
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取我的评论列表

    需要登录

    - **page**: 页码
    - **page_size**: 每页数量
    """
    service = CommentService(db)
    comments, total = await service.get_user_comments(
        current_user.id, page, page_size
    )

    # 转换为Response格式
    items = [CommentResponse.model_validate(c) for c in comments]

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
