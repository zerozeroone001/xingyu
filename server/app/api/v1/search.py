"""
搜索相关API
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from elasticsearch import AsyncElasticsearch

from app.core.database import get_db
from app.utils.elasticsearch_client import get_es_client
from app.services.search_service import SearchService
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/search")


@router.get("/poetries", response_model=ResponseModel[dict])
async def search_poetries(
    keyword: Optional[str] = Query(None, description="关键词"),
    dynasty: Optional[str] = Query(None, description="朝代"),
    type: Optional[str] = Query(None, description="类型"),
    tags: Optional[List[str]] = Query(None, description="标签"),
    author_name: Optional[str] = Query(None, description="作者名称"),
    page: int = Query(1, ge=1, description="页码"),
    page_size: int = Query(20, ge=1, le=100, description="每页数量"),
    sort_by: str = Query("_score", description="排序字段"),
    order: str = Query("desc", pattern="^(asc|desc)$", description="排序方式"),
    db: AsyncSession = Depends(get_db),
    es_client: AsyncElasticsearch = Depends(get_es_client),
):
    """
    搜索诗词（Elasticsearch全文搜索）

    - **keyword**: 关键词（搜索标题、内容、作者）
    - **dynasty**: 朝代筛选
    - **type**: 类型筛选
    - **tags**: 标签筛选
    - **author_name**: 作者名称
    - **page**: 页码
    - **page_size**: 每页数量
    - **sort_by**: 排序字段（_score, read_count, like_count, created_at）
    - **order**: 排序方式（asc, desc）
    """
    service = SearchService(db, es_client)

    result = await service.search_poetries(
        keyword=keyword,
        dynasty=dynasty,
        type_=type,
        tags=tags,
        author_name=author_name,
        page=page,
        page_size=page_size,
        sort_by=sort_by,
        order=order,
    )

    return ResponseModel(code=0, message="success", data=result)


@router.get("/suggest", response_model=ResponseModel[List[str]])
async def search_suggest(
    q: str = Query(..., min_length=1, description="搜索前缀"),
    size: int = Query(10, ge=1, le=20, description="返回数量"),
    db: AsyncSession = Depends(get_db),
    es_client: AsyncElasticsearch = Depends(get_es_client),
):
    """
    搜索建议

    - **q**: 搜索前缀
    - **size**: 返回数量
    """
    service = SearchService(db, es_client)
    suggestions = await service.suggest(q, size)

    return ResponseModel(code=0, message="success", data=suggestions)


@router.post("/index/rebuild", response_model=ResponseModel[dict])
async def rebuild_search_index(
    db: AsyncSession = Depends(get_db),
    es_client: AsyncElasticsearch = Depends(get_es_client),
):
    """
    重建搜索索引（管理员功能）

    批量索引所有诗词到Elasticsearch
    """
    service = SearchService(db, es_client)

    # 删除旧索引（如果存在）
    if await es_client.indices.exists(index=service.POETRY_INDEX):
        await es_client.indices.delete(index=service.POETRY_INDEX)

    # 创建新索引
    await service.create_poetry_index()

    # 批量索引
    await service.bulk_index_poetries()

    # 统计索引文档数
    count = await es_client.count(index=service.POETRY_INDEX)

    return ResponseModel(
        code=0,
        message="索引重建成功",
        data={"indexed_count": count["count"]},
    )
