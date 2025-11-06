"""
推荐相关API
"""

from typing import List
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.services.recommend_service import RecommendService
from app.schemas.poetry import PoetryDetail
from app.schemas.response import ResponseModel

router = APIRouter(prefix="/recommend")


@router.get("/hot", response_model=ResponseModel[List[PoetryDetail]])
async def get_hot_poetries(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    days: int = Query(7, ge=0, le=365, description="统计天数(0=全部)"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取热门诗词推荐

    基于综合热度算法：
    - like_count * 0.4
    - collect_count * 0.3
    - read_count * 0.2
    - comment_count * 0.1

    - **limit**: 返回数量（1-50）
    - **days**: 统计最近N天（0=全部时间）
    """
    service = RecommendService(db)
    poetries = await service.get_hot_poetries(limit, days)

    items = [PoetryDetail.model_validate(p) for p in poetries]

    return ResponseModel(
        code=0,
        message="success",
        data=items,
    )


@router.get("/random", response_model=ResponseModel[List[PoetryDetail]])
async def get_random_poetries(
    limit: int = Query(10, ge=1, le=50, description="返回数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取随机诗词推荐

    - **limit**: 返回数量（1-50）
    """
    service = RecommendService(db)
    poetries = await service.get_random_poetries(limit)

    items = [PoetryDetail.model_validate(p) for p in poetries]

    return ResponseModel(
        code=0,
        message="success",
        data=items,
    )


@router.get("/daily", response_model=ResponseModel[List[PoetryDetail]])
async def get_daily_recommend(
    limit: int = Query(10, ge=1, le=20, description="返回数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    每日推荐

    使用日期作为随机种子，同一天返回相同的推荐结果

    - **limit**: 返回数量（1-20）
    """
    service = RecommendService(db)
    poetries = await service.get_daily_recommend(limit)

    items = [PoetryDetail.model_validate(p) for p in poetries]

    return ResponseModel(
        code=0,
        message="success",
        data=items,
    )


@router.get("/similar/{poetry_id}", response_model=ResponseModel[List[PoetryDetail]])
async def get_similar_poetries(
    poetry_id: int,
    strategy: str = Query("dynasty", pattern="^(dynasty|author|type)$", description="相似策略"),
    limit: int = Query(10, ge=1, le=20, description="返回数量"),
    db: AsyncSession = Depends(get_db),
):
    """
    获取相似诗词推荐

    - **poetry_id**: 诗词ID
    - **strategy**: 相似策略
      * dynasty - 同朝代
      * author - 同作者
      * type - 同类型
    - **limit**: 返回数量（1-20）
    """
    service = RecommendService(db)

    if strategy == "dynasty":
        poetries = await service.get_similar_by_dynasty(poetry_id, limit)
    elif strategy == "author":
        poetries = await service.get_similar_by_author(poetry_id, limit)
    elif strategy == "type":
        poetries = await service.get_similar_by_type(poetry_id, limit)
    else:
        poetries = []

    items = [PoetryDetail.model_validate(p) for p in poetries]

    return ResponseModel(
        code=0,
        message="success",
        data=items,
    )


@router.get("/personalized", response_model=ResponseModel[List[PoetryDetail]])
async def get_personalized_recommend(
    limit: int = Query(20, ge=1, le=50, description="返回数量"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    个性化推荐（需要登录）

    根据用户的点赞和收藏行为分析偏好：
    - 分析喜欢的朝代、类型、作者
    - 推荐相似的诗词
    - 排除已互动的诗词

    - **limit**: 返回数量（1-50）
    """
    service = RecommendService(db)
    poetries = await service.get_personalized_recommend(current_user.id, limit)

    items = [PoetryDetail.model_validate(p) for p in poetries]

    return ResponseModel(
        code=0,
        message="success",
        data=items,
    )
