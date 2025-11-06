"""
用户诗词交互服务层
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.user_poetry_interaction import UserPoetryLike, UserPoetryCollection
from app.models.poetry import Poetry


class PoetryInteractionService:
    """诗词交互服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    # ============ 点赞相关 ============

    async def like_poetry(self, user_id: int, poetry_id: int) -> bool:
        """
        点赞诗词

        Args:
            user_id: 用户ID
            poetry_id: 诗词ID

        Returns:
            是否成功
        """
        # 检查是否已点赞
        existing = await self.db.execute(
            select(UserPoetryLike).where(
                and_(
                    UserPoetryLike.user_id == user_id,
                    UserPoetryLike.poetry_id == poetry_id,
                )
            )
        )
        if existing.scalar_one_or_none():
            return False  # 已点赞

        # 创建点赞记录
        like = UserPoetryLike(user_id=user_id, poetry_id=poetry_id)
        self.db.add(like)

        # 增加诗词点赞数
        poetry = await self.db.execute(
            select(Poetry).where(Poetry.id == poetry_id)
        )
        poetry_obj = poetry.scalar_one_or_none()
        if poetry_obj:
            poetry_obj.like_count = (poetry_obj.like_count or 0) + 1

        await self.db.commit()
        return True

    async def unlike_poetry(self, user_id: int, poetry_id: int) -> bool:
        """
        取消点赞诗词

        Args:
            user_id: 用户ID
            poetry_id: 诗词ID

        Returns:
            是否成功
        """
        # 删除点赞记录
        result = await self.db.execute(
            delete(UserPoetryLike).where(
                and_(
                    UserPoetryLike.user_id == user_id,
                    UserPoetryLike.poetry_id == poetry_id,
                )
            )
        )

        if result.rowcount == 0:
            return False  # 未点赞

        # 减少诗词点赞数
        poetry = await self.db.execute(
            select(Poetry).where(Poetry.id == poetry_id)
        )
        poetry_obj = poetry.scalar_one_or_none()
        if poetry_obj and poetry_obj.like_count > 0:
            poetry_obj.like_count -= 1

        await self.db.commit()
        return True

    async def check_liked(self, user_id: int, poetry_id: int) -> bool:
        """
        检查是否已点赞

        Args:
            user_id: 用户ID
            poetry_id: 诗词ID

        Returns:
            是否已点赞
        """
        result = await self.db.execute(
            select(UserPoetryLike).where(
                and_(
                    UserPoetryLike.user_id == user_id,
                    UserPoetryLike.poetry_id == poetry_id,
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_user_liked_poetries(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Poetry], int]:
        """
        获取用户点赞的诗词列表

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量

        Returns:
            (诗词列表, 总数)
        """
        # 构建查询
        query = (
            select(Poetry)
            .join(UserPoetryLike, UserPoetryLike.poetry_id == Poetry.id)
            .where(UserPoetryLike.user_id == user_id)
            .options(joinedload(Poetry.author))
            .order_by(UserPoetryLike.created_at.desc())
        )

        # 获取总数
        count_query = select(func.count()).select_from(
            select(Poetry.id)
            .join(UserPoetryLike, UserPoetryLike.poetry_id == Poetry.id)
            .where(UserPoetryLike.user_id == user_id)
            .subquery()
        )
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries), total

    # ============ 收藏相关 ============

    async def collect_poetry(self, user_id: int, poetry_id: int) -> bool:
        """
        收藏诗词

        Args:
            user_id: 用户ID
            poetry_id: 诗词ID

        Returns:
            是否成功
        """
        # 检查是否已收藏
        existing = await self.db.execute(
            select(UserPoetryCollection).where(
                and_(
                    UserPoetryCollection.user_id == user_id,
                    UserPoetryCollection.poetry_id == poetry_id,
                )
            )
        )
        if existing.scalar_one_or_none():
            return False  # 已收藏

        # 创建收藏记录
        collection = UserPoetryCollection(user_id=user_id, poetry_id=poetry_id)
        self.db.add(collection)

        # 增加诗词收藏数
        poetry = await self.db.execute(
            select(Poetry).where(Poetry.id == poetry_id)
        )
        poetry_obj = poetry.scalar_one_or_none()
        if poetry_obj:
            poetry_obj.collect_count = (poetry_obj.collect_count or 0) + 1

        await self.db.commit()
        return True

    async def uncollect_poetry(self, user_id: int, poetry_id: int) -> bool:
        """
        取消收藏诗词

        Args:
            user_id: 用户ID
            poetry_id: 诗词ID

        Returns:
            是否成功
        """
        # 删除收藏记录
        result = await self.db.execute(
            delete(UserPoetryCollection).where(
                and_(
                    UserPoetryCollection.user_id == user_id,
                    UserPoetryCollection.poetry_id == poetry_id,
                )
            )
        )

        if result.rowcount == 0:
            return False  # 未收藏

        # 减少诗词收藏数
        poetry = await self.db.execute(
            select(Poetry).where(Poetry.id == poetry_id)
        )
        poetry_obj = poetry.scalar_one_or_none()
        if poetry_obj and poetry_obj.collect_count > 0:
            poetry_obj.collect_count -= 1

        await self.db.commit()
        return True

    async def check_collected(self, user_id: int, poetry_id: int) -> bool:
        """
        检查是否已收藏

        Args:
            user_id: 用户ID
            poetry_id: 诗词ID

        Returns:
            是否已收藏
        """
        result = await self.db.execute(
            select(UserPoetryCollection).where(
                and_(
                    UserPoetryCollection.user_id == user_id,
                    UserPoetryCollection.poetry_id == poetry_id,
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_user_collected_poetries(
        self,
        user_id: int,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Poetry], int]:
        """
        获取用户收藏的诗词列表

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量

        Returns:
            (诗词列表, 总数)
        """
        # 构建查询
        query = (
            select(Poetry)
            .join(UserPoetryCollection, UserPoetryCollection.poetry_id == Poetry.id)
            .where(UserPoetryCollection.user_id == user_id)
            .options(joinedload(Poetry.author))
            .order_by(UserPoetryCollection.created_at.desc())
        )

        # 获取总数
        count_query = select(func.count()).select_from(
            select(Poetry.id)
            .join(UserPoetryCollection, UserPoetryCollection.poetry_id == Poetry.id)
            .where(UserPoetryCollection.user_id == user_id)
            .subquery()
        )
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        poetries = result.scalars().all()

        return list(poetries), total
