"""
诗词相关API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user, get_optional_current_user
from app.models.user import User
from app.services.poetry_service import PoetryService
from app.schemas.poetry import (
    PoetryCreate,
    PoetryUpdate,
    PoetryDetail,
    PoetryListItem,
    PoetryQuery,
)
from app.schemas.response import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/poetries")


@router.get("/", response_model=ResponseModel[PaginatedResponse[PoetryListItem]])
async def get_poetries(
    keyword: str = Query(None, description="关键词搜索"),
    dynasty: str = Query(None, description="朝代筛选"),
    type: str = Query(None, description="类型筛选"),
    author_id: int = Query(None, description="作者ID筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    sort_by: str = Query("created_at", description="排序字段"),
    order: str = Query("desc", description="排序方式"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取诗词列表

    - **keyword**: 关键词搜索（标题、内容）
    - **dynasty**: 朝代筛选
    - **type**: 类型筛选
    - **author_id**: 作者ID筛选
    - **page**: 页码
    - **page_size**: 每页数量
    - **sort_by**: 排序字段（created_at, read_count, like_count）
    - **order**: 排序方式（asc, desc）
    """
    query_params = PoetryQuery(
        keyword=keyword,
        dynasty=dynasty,
        type=type,
        author_id=author_id,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        order=order,
    )

    service = PoetryService(db)
    poetries, total = await service.get_list(query_params)

    # 转换为ListItem格式
    items = [PoetryListItem.model_validate(p) for p in poetries]

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


@router.get("/random", response_model=ResponseModel[List[PoetryDetail]])
async def get_random_poetries(
    limit: int = Query(1, ge=1, le=10, description="数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    随机获取诗词

    - **limit**: 数量（1-10）
    """
    service = PoetryService(db)
    poetries = await service.get_random(limit)

    items = [PoetryDetail.model_validate(p) for p in poetries]

    return ResponseModel(
        code=200,
        msg="success",
        data=items,
    )


@router.get("/hot", response_model=ResponseModel[List[PoetryDetail]])
async def get_hot_poetries(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取热门诗词

    - **limit**: 数量（1-50）
    """
    service = PoetryService(db)
    poetries = await service.get_hot_poetries(limit)

    items = [PoetryDetail.model_validate(p) for p in poetries]

    return ResponseModel(
        code=200,
        msg="success",
        data=items,
    )


@router.get("/{poetry_id}", response_model=ResponseModel[PoetryDetail])
async def get_poetry_detail(
    poetry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_optional_current_user),
):
    """
    获取诗词详情

    - **poetry_id**: 诗词ID

    自动增加阅读数
    """
    service = PoetryService(db)

    # 获取诗词详情
    poetry = await service.get_by_id(poetry_id)
    if not poetry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="诗词不存在",
        )

    # 增加阅读数
    await service.increment_read_count(poetry_id)

    return ResponseModel(
        code=200,
        msg="success",
        data=PoetryDetail.model_validate(poetry),
    )


@router.post("/", response_model=ResponseModel[PoetryDetail], status_code=status.HTTP_201_CREATED)
async def create_poetry(
    poetry_data: PoetryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建诗词

    需要登录
    """
    service = PoetryService(db)
    poetry = await service.create(poetry_data)

    return ResponseModel(
        code=200,
        msg="创建成功",
        data=PoetryDetail.model_validate(poetry),
    )


@router.put("/{poetry_id}", response_model=ResponseModel[PoetryDetail])
async def update_poetry(
    poetry_id: int,
    poetry_data: PoetryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新诗词

    需要登录
    """
    service = PoetryService(db)
    poetry = await service.update(poetry_id, poetry_data)

    if not poetry:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="诗词不存在",
        )

    return ResponseModel(
        code=200,
        msg="更新成功",
        data=PoetryDetail.model_validate(poetry),
    )


@router.delete("/{poetry_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_poetry(
    poetry_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除诗词

    需要登录
    """
    service = PoetryService(db)
    success = await service.delete(poetry_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="诗词不存在",
        )

    return None
