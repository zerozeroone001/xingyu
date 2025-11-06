"""
作者相关API
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.author_service import AuthorService
from app.schemas.author import (
    AuthorCreate,
    AuthorUpdate,
    AuthorResponse,
    AuthorSimple,
)
from app.schemas.response import ResponseModel, PaginatedResponse

router = APIRouter(prefix="/authors")


@router.get("/", response_model=ResponseModel[PaginatedResponse[AuthorResponse]])
async def get_authors(
    keyword: str = Query(None, description="关键词搜索"),
    dynasty: str = Query(None, description="朝代筛选"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    sort_by: str = Query("id", description="排序字段"),
    order: str = Query("desc", description="排序方式"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取作者列表

    - **keyword**: 关键词搜索（姓名、简介）
    - **dynasty**: 朝代筛选
    - **page**: 页码
    - **page_size**: 每页数量
    - **sort_by**: 排序字段（id, name, birth_year）
    - **order**: 排序方式（asc, desc）
    """
    service = AuthorService(db)
    authors, total = await service.get_list(
        keyword=keyword,
        dynasty=dynasty,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        order=order,
    )

    # 转换为Response格式
    items = [AuthorResponse.model_validate(a) for a in authors]

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


@router.get("/hot", response_model=ResponseModel[List[AuthorSimple]])
async def get_hot_authors(
    limit: int = Query(10, ge=1, le=50, description="数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取热门作者

    - **limit**: 数量（1-50）
    """
    service = AuthorService(db)
    authors = await service.get_hot_authors(limit)

    items = [AuthorSimple.model_validate(a) for a in authors]

    return ResponseModel(
        code=0,
        message="success",
        data=items,
    )


@router.get("/dynasty/{dynasty}", response_model=ResponseModel[List[AuthorResponse]])
async def get_authors_by_dynasty(
    dynasty: str,
    db: AsyncSession = Depends(get_db),
):
    """
    按朝代获取作者列表

    - **dynasty**: 朝代名称
    """
    service = AuthorService(db)
    authors = await service.search_by_dynasty(dynasty)

    items = [AuthorResponse.model_validate(a) for a in authors]

    return ResponseModel(
        code=0,
        message="success",
        data=items,
    )


@router.get("/{author_id}", response_model=ResponseModel[AuthorResponse])
async def get_author_detail(
    author_id: int,
    db: AsyncSession = Depends(get_db),
):
    """
    获取作者详情

    - **author_id**: 作者ID
    """
    service = AuthorService(db)
    author = await service.get_by_id(author_id)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作者不存在",
        )

    return ResponseModel(
        code=0,
        message="success",
        data=AuthorResponse.model_validate(author),
    )


@router.post("/", response_model=ResponseModel[AuthorResponse], status_code=status.HTTP_201_CREATED)
async def create_author(
    author_data: AuthorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    创建作者

    需要登录
    """
    service = AuthorService(db)

    # 检查作者是否已存在
    existing = await service.get_by_name(author_data.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该作者已存在",
        )

    author = await service.create(author_data)

    return ResponseModel(
        code=0,
        message="创建成功",
        data=AuthorResponse.model_validate(author),
    )


@router.put("/{author_id}", response_model=ResponseModel[AuthorResponse])
async def update_author(
    author_id: int,
    author_data: AuthorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    更新作者

    需要登录
    """
    service = AuthorService(db)
    author = await service.update(author_id, author_data)

    if not author:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作者不存在",
        )

    return ResponseModel(
        code=0,
        message="更新成功",
        data=AuthorResponse.model_validate(author),
    )


@router.delete("/{author_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_author(
    author_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    删除作者

    需要登录
    """
    service = AuthorService(db)
    success = await service.delete(author_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="作者不存在",
        )

    return None
