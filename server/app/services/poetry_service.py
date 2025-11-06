"""
诗词业务逻辑服务
"""

from typing import Optional, List, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, or_, and_
from sqlalchemy.orm import joinedload

from app.models.poetry import Poetry
from app.models.author import Author
from app.schemas.poetry import PoetryCreate, PoetryUpdate, PoetryQuery


class PoetryService:
    """诗词服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        query_params: PoetryQuery
    ) -> Tuple[List[Poetry], int]:
        """
        获取诗词列表

        Args:
            query_params: 查询参数

        Returns:
            (诗词列表, 总数)
        """
        # 构建查询
        stmt = select(Poetry).options(joinedload(Poetry.author))

        # 只查询已发布的诗词
        stmt = stmt.where(Poetry.status == 1)

        # 关键词搜索
        if query_params.keyword:
            keyword = f"%{query_params.keyword}%"
            stmt = stmt.where(
                or_(
                    Poetry.title.like(keyword),
                    Poetry.content.like(keyword)
                )
            )

        # 朝代筛选
        if query_params.dynasty:
            stmt = stmt.where(Poetry.dynasty == query_params.dynasty)

        # 类型筛选
        if query_params.type:
            stmt = stmt.where(Poetry.type == query_params.type)

        # 作者筛选
        if query_params.author_id:
            stmt = stmt.where(Poetry.author_id == query_params.author_id)

        # 统计总数
        count_stmt = select(func.count()).select_from(stmt.subquery())
        total_result = await self.db.execute(count_stmt)
        total = total_result.scalar() or 0

        # 排序
        if query_params.sort_by == "read_count":
            order_column = Poetry.read_count
        elif query_params.sort_by == "like_count":
            order_column = Poetry.like_count
        elif query_params.sort_by == "comment_count":
            order_column = Poetry.comment_count
        else:
            order_column = Poetry.created_at

        if query_params.order == "asc":
            stmt = stmt.order_by(order_column.asc())
        else:
            stmt = stmt.order_by(order_column.desc())

        # 分页
        offset = (query_params.page - 1) * query_params.page_size
        stmt = stmt.offset(offset).limit(query_params.page_size)

        # 执行查询
        result = await self.db.execute(stmt)
        poetries = result.scalars().all()

        return list(poetries), total

    async def get_by_id(self, poetry_id: int) -> Optional[Poetry]:
        """
        根据ID获取诗词详情

        Args:
            poetry_id: 诗词ID

        Returns:
            诗词对象或None
        """
        stmt = select(Poetry).options(joinedload(Poetry.author)).where(
            Poetry.id == poetry_id,
            Poetry.status == 1
        )
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def create(self, poetry_data: PoetryCreate) -> Poetry:
        """
        创建诗词

        Args:
            poetry_data: 诗词数据

        Returns:
            创建的诗词对象
        """
        poetry = Poetry(**poetry_data.model_dump())
        self.db.add(poetry)
        await self.db.commit()
        await self.db.refresh(poetry)

        # 加载作者信息
        if poetry.author_id:
            await self.db.refresh(poetry, ["author"])

        return poetry

    async def update(
        self,
        poetry_id: int,
        poetry_data: PoetryUpdate
    ) -> Optional[Poetry]:
        """
        更新诗词

        Args:
            poetry_id: 诗词ID
            poetry_data: 更新数据

        Returns:
            更新后的诗词对象或None
        """
        poetry = await self.get_by_id(poetry_id)
        if not poetry:
            return None

        # 更新字段
        update_data = poetry_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(poetry, field, value)

        await self.db.commit()
        await self.db.refresh(poetry)

        # 重新加载作者信息
        if poetry.author_id:
            await self.db.refresh(poetry, ["author"])

        return poetry

    async def delete(self, poetry_id: int) -> bool:
        """
        删除诗词（软删除）

        Args:
            poetry_id: 诗词ID

        Returns:
            是否成功
        """
        poetry = await self.get_by_id(poetry_id)
        if not poetry:
            return False

        poetry.status = 3  # 标记为已删除
        await self.db.commit()
        return True

    async def increment_read_count(self, poetry_id: int) -> bool:
        """
        增加阅读数

        Args:
            poetry_id: 诗词ID

        Returns:
            是否成功
        """
        stmt = select(Poetry).where(Poetry.id == poetry_id)
        result = await self.db.execute(stmt)
        poetry = result.scalar_one_or_none()

        if not poetry:
            return False

        poetry.read_count += 1
        await self.db.commit()
        return True

    async def get_random(self, limit: int = 1) -> List[Poetry]:
        """
        随机获取诗词

        Args:
            limit: 数量

        Returns:
            诗词列表
        """
        stmt = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(Poetry.status == 1)
            .order_by(func.random())
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())

    async def get_hot_poetries(self, limit: int = 10) -> List[Poetry]:
        """
        获取热门诗词

        Args:
            limit: 数量

        Returns:
            诗词列表
        """
        stmt = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(Poetry.status == 1)
            .order_by(
                (Poetry.read_count + Poetry.like_count * 2 + Poetry.comment_count * 3)
                .desc()
            )
            .limit(limit)
        )
        result = await self.db.execute(stmt)
        return list(result.scalars().all())
