"""
诗词相关Schema
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from app.schemas.author import AuthorSimple


class PoetryBase(BaseModel):
    """诗词基础Schema"""

    title: str = Field(..., min_length=1, max_length=100, description="标题")
    content: str = Field(..., min_length=1, description="内容")
    author_id: Optional[int] = Field(None, description="作者ID")
    dynasty: Optional[str] = Field(None, max_length=50, description="朝代")
    type: Optional[str] = Field(None, max_length=50, description="类型")
    tags: Optional[List[str]] = Field(None, description="标签")
    translation: Optional[str] = Field(None, description="翻译")
    annotation: Optional[str] = Field(None, description="注释")
    appreciation: Optional[str] = Field(None, description="赏析")
    background: Optional[str] = Field(None, description="创作背景")


class PoetryCreate(PoetryBase):
    """创建诗词Schema"""
    pass


class PoetryUpdate(BaseModel):
    """更新诗词Schema"""

    title: Optional[str] = Field(None, min_length=1, max_length=100, description="标题")
    content: Optional[str] = Field(None, min_length=1, description="内容")
    author_id: Optional[int] = Field(None, description="作者ID")
    dynasty: Optional[str] = Field(None, max_length=50, description="朝代")
    type: Optional[str] = Field(None, max_length=50, description="类型")
    tags: Optional[List[str]] = Field(None, description="标签")
    translation: Optional[str] = Field(None, description="翻译")
    annotation: Optional[str] = Field(None, description="注释")
    appreciation: Optional[str] = Field(None, description="赏析")
    background: Optional[str] = Field(None, description="创作背景")
    status: Optional[int] = Field(None, ge=1, le=3, description="状态")


class PoetryListItem(BaseModel):
    """诗词列表项Schema"""

    id: int = Field(..., description="诗词ID")
    title: str = Field(..., description="标题")
    content: str = Field(..., description="内容（可能是摘要）")
    author: Optional[AuthorSimple] = Field(None, description="作者信息")
    dynasty: Optional[str] = Field(None, description="朝代")
    type: Optional[str] = Field(None, description="类型")
    read_count: int = Field(..., description="阅读数")
    like_count: int = Field(..., description="点赞数")
    comment_count: int = Field(..., description="评论数")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "静夜思",
                "content": "床前明月光，疑是地上霜...",
                "author": {"id": 1, "name": "李白", "dynasty": "唐代"},
                "dynasty": "唐代",
                "type": "五言绝句",
                "read_count": 1000,
                "like_count": 50,
                "comment_count": 20,
                "created_at": "2024-01-01T00:00:00"
            }
        }


class PoetryDetail(PoetryBase):
    """诗词详情Schema"""

    id: int = Field(..., description="诗词ID")
    author: Optional[AuthorSimple] = Field(None, description="作者信息")
    read_count: int = Field(..., description="阅读数")
    like_count: int = Field(..., description="点赞数")
    comment_count: int = Field(..., description="评论数")
    collect_count: int = Field(..., description="收藏数")
    status: int = Field(..., description="状态")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "静夜思",
                "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
                "author": {"id": 1, "name": "李白", "dynasty": "唐代"},
                "dynasty": "唐代",
                "type": "五言绝句",
                "tags": ["思乡", "明月"],
                "translation": "明亮的月光洒在床前...",
                "annotation": "疑：好像。举头：抬头。",
                "appreciation": "这首诗表达了诗人对故乡的思念之情...",
                "read_count": 1000,
                "like_count": 50,
                "comment_count": 20,
                "collect_count": 30,
                "status": 1,
                "created_at": "2024-01-01T00:00:00",
                "updated_at": "2024-01-01T00:00:00"
            }
        }


class PoetryResponse(PoetryDetail):
    """诗词响应Schema（别名）"""
    pass


class PoetryQuery(BaseModel):
    """诗词查询Schema"""

    keyword: Optional[str] = Field(None, description="关键词搜索")
    dynasty: Optional[str] = Field(None, description="朝代筛选")
    type: Optional[str] = Field(None, description="类型筛选")
    author_id: Optional[int] = Field(None, description="作者ID筛选")
    page: int = Field(default=1, ge=1, description="页码")
    page_size: int = Field(default=20, ge=1, le=100, description="每页数量")
    sort_by: Optional[str] = Field(
        default="created_at",
        description="排序字段: created_at, read_count, like_count"
    )
    order: Optional[str] = Field(
        default="desc",
        description="排序方式: asc, desc"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "keyword": "明月",
                "dynasty": "唐代",
                "type": "五言绝句",
                "page": 1,
                "page_size": 20,
                "sort_by": "read_count",
                "order": "desc"
            }
        }
