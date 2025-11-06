"""
推荐服务层
"""

from typing import List, Tuple
from datetime import datetime, timedelta
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.poetry import Poetry
from app.models.user import User
from app.models.user_poetry_interaction import UserPoetryLike, UserPoetryCollection


class RecommendService:
    """推荐服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_hot_poetries(
        self, limit: int = 10, days: int = 7
    ) -> List[Poetry]:
        """
        获取热门诗词（基于综合热度）

        热度算法：like_count * 0.4 + collect_count * 0.3 + read_count * 0.2 + comment_count * 0.1

        Args:
            limit: 返回数量
            days: 统计最近N天（0=全部）

        Returns:
            诗词列表
        """
        query = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(Poetry.status == 1)
        )

        # 如果指定天数，只查询最近N天的
        if days > 0:
            since_date = datetime.utcnow() - timedelta(days=days)
            query = query.where(Poetry.created_at >= since_date)

        # 按热度排序
        query = query.order_by(
            desc(
                (Poetry.like_count * 0.4)
                + (Poetry.collect_count * 0.3)
                + (Poetry.read_count * 0.2)
                + (Poetry.comment_count * 0.1)
            )
        ).limit(limit)

        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries)

    async def get_random_poetries(
        self, limit: int = 10, exclude_ids: List[int] = None
    ) -> List[Poetry]:
        """
        获取随机诗词

        Args:
            limit: 返回数量
            exclude_ids: 排除的诗词ID列表

        Returns:
            诗词列表
        """
        query = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(Poetry.status == 1)
        )

        if exclude_ids:
            query = query.where(Poetry.id.notin_(exclude_ids))

        # 随机排序
        query = query.order_by(func.rand()).limit(limit)

        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries)

    async def get_daily_recommend(self, limit: int = 10) -> List[Poetry]:
        """
        每日推荐（基于日期种子的随机）

        使用日期作为随机种子，保证同一天返回相同的结果

        Args:
            limit: 返回数量

        Returns:
            诗词列表
        """
        # 使用当前日期作为种子
        today = datetime.utcnow().date()
        seed = int(today.strftime("%Y%m%d"))

        query = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(Poetry.status == 1)
            .order_by(func.rand(seed))
            .limit(limit)
        )

        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries)

    async def get_similar_by_dynasty(
        self, poetry_id: int, limit: int = 10
    ) -> List[Poetry]:
        """
        获取同朝代的相似诗词

        Args:
            poetry_id: 诗词ID
            limit: 返回数量

        Returns:
            诗词列表
        """
        # 获取目标诗词
        result = await self.db.execute(
            select(Poetry).where(Poetry.id == poetry_id)
        )
        target_poetry = result.scalar_one_or_none()

        if not target_poetry:
            return []

        # 查询同朝代的诗词
        query = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(
                and_(
                    Poetry.status == 1,
                    Poetry.dynasty == target_poetry.dynasty,
                    Poetry.id != poetry_id,
                )
            )
            .order_by(desc(Poetry.like_count))
            .limit(limit)
        )

        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries)

    async def get_similar_by_author(
        self, poetry_id: int, limit: int = 10
    ) -> List[Poetry]:
        """
        获取同作者的其他诗词

        Args:
            poetry_id: 诗词ID
            limit: 返回数量

        Returns:
            诗词列表
        """
        # 获取目标诗词
        result = await self.db.execute(
            select(Poetry).where(Poetry.id == poetry_id)
        )
        target_poetry = result.scalar_one_or_none()

        if not target_poetry or not target_poetry.author_id:
            return []

        # 查询同作者的其他诗词
        query = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(
                and_(
                    Poetry.status == 1,
                    Poetry.author_id == target_poetry.author_id,
                    Poetry.id != poetry_id,
                )
            )
            .order_by(desc(Poetry.like_count))
            .limit(limit)
        )

        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries)

    async def get_similar_by_type(
        self, poetry_id: int, limit: int = 10
    ) -> List[Poetry]:
        """
        获取同类型的诗词

        Args:
            poetry_id: 诗词ID
            limit: 返回数量

        Returns:
            诗词列表
        """
        # 获取目标诗词
        result = await self.db.execute(
            select(Poetry).where(Poetry.id == poetry_id)
        )
        target_poetry = result.scalar_one_or_none()

        if not target_poetry or not target_poetry.type:
            return []

        # 查询同类型的诗词
        query = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(
                and_(
                    Poetry.status == 1,
                    Poetry.type == target_poetry.type,
                    Poetry.id != poetry_id,
                )
            )
            .order_by(desc(Poetry.like_count))
            .limit(limit)
        )

        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries)

    async def get_personalized_recommend(
        self, user_id: int, limit: int = 20
    ) -> List[Poetry]:
        """
        个性化推荐（基于用户行为）

        根据用户点赞和收藏的诗词，推荐相似的内容

        Args:
            user_id: 用户ID
            limit: 返回数量

        Returns:
            诗词列表
        """
        # 获取用户点赞和收藏的诗词
        liked_result = await self.db.execute(
            select(UserPoetryLike.poetry_id)
            .where(UserPoetryLike.user_id == user_id)
            .order_by(UserPoetryLike.created_at.desc())
            .limit(10)
        )
        liked_ids = [row[0] for row in liked_result.all()]

        collected_result = await self.db.execute(
            select(UserPoetryCollection.poetry_id)
            .where(UserPoetryCollection.user_id == user_id)
            .order_by(UserPoetryCollection.created_at.desc())
            .limit(10)
        )
        collected_ids = [row[0] for row in collected_result.all()]

        # 合并并去重
        user_poetry_ids = list(set(liked_ids + collected_ids))

        if not user_poetry_ids:
            # 如果用户没有互动记录，返回热门推荐
            return await self.get_hot_poetries(limit)

        # 获取用户喜欢的诗词
        user_poetries_result = await self.db.execute(
            select(Poetry).where(Poetry.id.in_(user_poetry_ids))
        )
        user_poetries = user_poetries_result.scalars().all()

        # 统计用户偏好
        dynasties = {}
        types = {}
        authors = {}

        for poetry in user_poetries:
            if poetry.dynasty:
                dynasties[poetry.dynasty] = dynasties.get(poetry.dynasty, 0) + 1
            if poetry.type:
                types[poetry.type] = types.get(poetry.type, 0) + 1
            if poetry.author_id:
                authors[poetry.author_id] = authors.get(poetry.author_id, 0) + 1

        # 找出最喜欢的朝代、类型、作者
        favorite_dynasty = max(dynasties.items(), key=lambda x: x[1])[0] if dynasties else None
        favorite_type = max(types.items(), key=lambda x: x[1])[0] if types else None
        favorite_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:3]
        favorite_author_ids = [author_id for author_id, _ in favorite_authors]

        # 构建推荐查询
        conditions = []

        if favorite_dynasty:
            conditions.append(Poetry.dynasty == favorite_dynasty)

        if favorite_type:
            conditions.append(Poetry.type == favorite_type)

        if favorite_author_ids:
            conditions.append(Poetry.author_id.in_(favorite_author_ids))

        if not conditions:
            # 如果没有明显偏好，返回热门推荐
            return await self.get_hot_poetries(limit)

        # 查询推荐诗词
        query = (
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(
                and_(
                    Poetry.status == 1,
                    Poetry.id.notin_(user_poetry_ids),  # 排除已互动的
                    or_(*conditions),
                )
            )
            .order_by(desc(Poetry.like_count))
            .limit(limit)
        )

        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries)
