"""
消息相关API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.message_service import MessageService
from app.schemas.message import MessageResponse, MessageStats
from app.schemas.response import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/messages")


@router.get("", response_model=ResponseModel[PaginatedResponse[MessageResponse]])
async def get_messages(
    type_: str = Query(None, alias="type", description="消息类型筛选"),
    is_read: int = Query(None, ge=0, le=1, description="读取状态"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取消息列表（需要登录）

    - **type**: 消息类型筛选（system/like/comment/follow/collect）
    - **is_read**: 读取状态（0未读/1已读）
    - **page**: 页码
    - **page_size**: 每页数量（1-100）
    """
    service = MessageService(db)
    messages, total = await service.get_list(
        user_id=current_user.id,
        type_=type_,
        is_read=is_read,
        page=page,
        page_size=page_size,
    )

    items = [MessageResponse.model_validate(m) for m in messages]

    return ResponseModel(
        code=200,
        msg="success",
        data=PaginatedResponse(
            list=items,
            total=total,
            page=page,
            page_size=page_size,
        ),
    )


@router.get("/stats", response_model=ResponseModel[MessageStats])
async def get_message_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取消息统计（需要登录）

    返回各类型消息的未读数量
    """
    service = MessageService(db)
    stats = await service.get_stats(current_user.id)

    return ResponseModel(
        code=200,
        msg="success",
        data=MessageStats(**stats),
    )


@router.get("/unread-count", response_model=ResponseModel[int])
async def get_unread_count(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取未读消息数（需要登录）
    """
    service = MessageService(db)
    count = await service.get_unread_count(current_user.id)

    return ResponseModel(
        code=200,
        msg="success",
        data=count,
    )


@router.get("/{message_id}", response_model=ResponseModel[MessageResponse])
async def get_message_detail(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    获取消息详情（需要登录）

    - **message_id**: 消息ID
    """
    service = MessageService(db)
    message = await service.get_by_id(message_id, current_user.id)

    if not message:
        raise HTTPException(status_code=404, detail="消息不存在")

    return ResponseModel(
        code=200,
        msg="success",
        data=MessageResponse.model_validate(message),
    )


@router.put("/{message_id}/read", response_model=ResponseModel[None])
async def mark_message_as_read(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    标记消息为已读（需要登录）

    - **message_id**: 消息ID
    """
    service = MessageService(db)
    success = await service.mark_as_read(message_id, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="消息不存在")

    return ResponseModel(
        code=200,
        msg="标记成功",
        data=None,
    )


@router.put("/read-all", response_model=ResponseModel[int])
async def mark_all_as_read(
    type_: str = Query(None, alias="type", description="消息类型"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    标记所有消息为已读（需要登录）

    - **type**: 消息类型（可选，为空则标记全部）
    """
    service = MessageService(db)
    count = await service.mark_all_as_read(current_user.id, type_)

    return ResponseModel(
        code=200,
        message=f"已标记{count}条消息为已读",
        data=count,
    )


@router.delete("/{message_id}", response_model=ResponseModel[None])
async def delete_message(
    message_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除消息（需要登录）

    - **message_id**: 消息ID
    """
    service = MessageService(db)
    success = await service.delete(message_id, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="消息不存在")

    return ResponseModel(
        code=200,
        msg="删除成功",
        data=None,
    )
