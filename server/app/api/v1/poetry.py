"""
诗词相关API
"""

from fastapi import APIRouter

router = APIRouter(prefix="/poetries")


@router.get("/")
async def get_poetries():
    """
    获取诗词列表
    （开发中）
    """
    return {
        "code": 0,
        "message": "诗词列表功能开发中",
        "data": {"items": [], "total": 0},
    }


@router.get("/{poetry_id}")
async def get_poetry_detail(poetry_id: int):
    """
    获取诗词详情
    （开发中）
    """
    return {
        "code": 0,
        "message": "诗词详情功能开发中",
        "data": {"id": poetry_id},
    }
