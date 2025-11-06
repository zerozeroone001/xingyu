"""
关注服务层
"""

from typing import List, Tuple
from sqlalchemy import select, func, and_, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.follow import Follow
from app.models.user import User


class FollowService:
    """关注服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def follow_user(self, user_id: int, follow_user_id: int) -> bool:
        """
        关注用户

        Args:
            user_id: 关注者ID
            follow_user_id: 被关注者ID

        Returns:
            是否成功
        """
        # 不能关注自己
        if user_id == follow_user_id:
            return False

        # 检查是否已关注
        existing = await self.db.execute(
            select(Follow).where(
                and_(
                    Follow.user_id == user_id,
                    Follow.follow_user_id == follow_user_id,
                )
            )
        )
        if existing.scalar_one_or_none():
            return False  # 已关注

        # 创建关注记录
        follow = Follow(user_id=user_id, follow_user_id=follow_user_id)
        self.db.add(follow)
        await self.db.commit()
        return True

    async def unfollow_user(self, user_id: int, follow_user_id: int) -> bool:
        """
        取消关注用户

        Args:
            user_id: 关注者ID
            follow_user_id: 被关注者ID

        Returns:
            是否成功
        """
        # 删除关注记录
        result = await self.db.execute(
            delete(Follow).where(
                and_(
                    Follow.user_id == user_id,
                    Follow.follow_user_id == follow_user_id,
                )
            )
        )

        await self.db.commit()
        return result.rowcount > 0

    async def check_following(self, user_id: int, follow_user_id: int) -> bool:
        """
        检查是否已关注

        Args:
            user_id: 关注者ID
            follow_user_id: 被关注者ID

        Returns:
            是否已关注
        """
        result = await self.db.execute(
            select(Follow).where(
                and_(
                    Follow.user_id == user_id,
                    Follow.follow_user_id == follow_user_id,
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def get_following_list(
        self, user_id: int, page: int = 1, page_size: int = 20
    ) -> Tuple[List[User], int]:
        """
        获取关注列表

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量

        Returns:
            (用户列表, 总数)
        """
        # 构建查询
        query = (
            select(User)
            .join(Follow, Follow.follow_user_id == User.id)
            .where(Follow.user_id == user_id)
            .order_by(Follow.created_at.desc())
        )

        # 获取总数
        count_query = select(func.count()).select_from(
            select(User.id)
            .join(Follow, Follow.follow_user_id == User.id)
            .where(Follow.user_id == user_id)
            .subquery()
        )
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        users = result.scalars().all()

        return list(users), total

    async def get_followers_list(
        self, user_id: int, page: int = 1, page_size: int = 20
    ) -> Tuple[List[User], int]:
        """
        获取粉丝列表

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量

        Returns:
            (用户列表, 总数)
        """
        # 构建查询
        query = (
            select(User)
            .join(Follow, Follow.user_id == User.id)
            .where(Follow.follow_user_id == user_id)
            .order_by(Follow.created_at.desc())
        )

        # 获取总数
        count_query = select(func.count()).select_from(
            select(User.id)
            .join(Follow, Follow.user_id == User.id)
            .where(Follow.follow_user_id == user_id)
            .subquery()
        )
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        users = result.scalars().all()

        return list(users), total

    async def get_following_count(self, user_id: int) -> int:
        """
        获取关注数

        Args:
            user_id: 用户ID

        Returns:
            关注数
        """
        result = await self.db.execute(
            select(func.count()).select_from(Follow).where(Follow.user_id == user_id)
        )
        return result.scalar()

    async def get_followers_count(self, user_id: int) -> int:
        """
        获取粉丝数

        Args:
            user_id: 用户ID

        Returns:
            粉丝数
        """
        result = await self.db.execute(
            select(func.count())
            .select_from(Follow)
            .where(Follow.follow_user_id == user_id)
        )
        return result.scalar()

    async def get_mutual_following(
        self, user_id: int, page: int = 1, page_size: int = 20
    ) -> Tuple[List[User], int]:
        """
        获取互相关注列表（好友）

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量

        Returns:
            (用户列表, 总数)
        """
        # 查询互相关注的用户ID
        # 用户A关注的人中，同时也关注了用户A的人
        subquery = (
            select(Follow.follow_user_id)
            .where(
                and_(
                    Follow.user_id == user_id,
                    Follow.follow_user_id.in_(
                        select(Follow.user_id).where(Follow.follow_user_id == user_id)
                    ),
                )
            )
            .subquery()
        )

        # 构建查询
        query = select(User).where(User.id.in_(select(subquery)))

        # 获取总数
        count_query = select(func.count()).select_from(subquery)
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        users = result.scalars().all()

        return list(users), total
