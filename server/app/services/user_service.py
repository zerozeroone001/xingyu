"""
用户服务层
"""
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_, or_
from sqlalchemy.orm import selectinload

from app.models.user import User
from app.models.follow import Follow
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """用户服务类"""

    async def get_user(self, db: AsyncSession, user_id: int) -> Optional[User]:
        """
        获取用户信息

        Args:
            db: 数据库会话
            user_id: 用户ID

        Returns:
            用户对象或None
        """
        result = await db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def get_user_by_username(self, db: AsyncSession, username: str) -> Optional[User]:
        """
        通过用户名获取用户

        Args:
            db: 数据库会话
            username: 用户名

        Returns:
            用户对象或None
        """
        result = await db.execute(
            select(User).where(User.username == username)
        )
        return result.scalar_one_or_none()

    async def get_user_by_email(self, db: AsyncSession, email: str) -> Optional[User]:
        """
        通过邮箱获取用户

        Args:
            db: 数据库会话
            email: 邮箱地址

        Returns:
            用户对象或None
        """
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_users(
        self,
        db: AsyncSession,
        skip: int = 0,
        limit: int = 20
    ) -> List[User]:
        """
        获取用户列表

        Args:
            db: 数据库会话
            skip: 跳过数量
            limit: 限制数量

        Returns:
            用户列表
        """
        result = await db.execute(
            select(User)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def create_user(self, db: AsyncSession, user_create: UserCreate) -> User:
        """
        创建用户

        Args:
            db: 数据库会话
            user_create: 用户创建数据

        Returns:
            创建的用户对象
        """
        user = User(**user_create.dict())
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user

    async def update_user(
        self,
        db: AsyncSession,
        user_id: int,
        user_update: UserUpdate
    ) -> Optional[User]:
        """
        更新用户信息

        Args:
            db: 数据库会话
            user_id: 用户ID
            user_update: 用户更新数据

        Returns:
            更新后的用户对象或None
        """
        user = await self.get_user(db, user_id)
        if not user:
            return None

        update_data = user_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await db.commit()
        await db.refresh(user)
        return user

    async def delete_user(self, db: AsyncSession, user_id: int) -> bool:
        """
        删除用户

        Args:
            db: 数据库会话
            user_id: 用户ID

        Returns:
            是否删除成功
        """
        user = await self.get_user(db, user_id)
        if not user:
            return False

        await db.delete(user)
        await db.commit()
        return True

    async def get_user_stats(self, db: AsyncSession, user_id: int) -> dict:
        """
        获取用户统计信息

        Args:
            db: 数据库会话
            user_id: 用户ID

        Returns:
            统计信息字典
        """
        # 获取关注数
        following_count_result = await db.execute(
            select(func.count(Follow.id))
            .where(Follow.follower_id == user_id)
        )
        following_count = following_count_result.scalar() or 0

        # 获取粉丝数
        followers_count_result = await db.execute(
            select(func.count(Follow.id))
            .where(Follow.following_id == user_id)
        )
        followers_count = followers_count_result.scalar() or 0

        return {
            "following_count": following_count,
            "followers_count": followers_count,
        }

    async def check_follow_status(
        self,
        db: AsyncSession,
        follower_id: int,
        following_id: int
    ) -> bool:
        """
        检查关注状态

        Args:
            db: 数据库会话
            follower_id: 关注者ID
            following_id: 被关注者ID

        Returns:
            是否已关注
        """
        result = await db.execute(
            select(Follow)
            .where(
                and_(
                    Follow.follower_id == follower_id,
                    Follow.following_id == following_id
                )
            )
        )
        return result.scalar_one_or_none() is not None

    async def follow_user(
        self,
        db: AsyncSession,
        follower_id: int,
        following_id: int
    ) -> bool:
        """
        关注用户

        Args:
            db: 数据库会话
            follower_id: 关注者ID
            following_id: 被关注者ID

        Returns:
            是否关注成功
        """
        # 检查是否已关注
        if await self.check_follow_status(db, follower_id, following_id):
            return False

        # 不能关注自己
        if follower_id == following_id:
            return False

        follow = Follow(follower_id=follower_id, following_id=following_id)
        db.add(follow)
        await db.commit()
        return True

    async def unfollow_user(
        self,
        db: AsyncSession,
        follower_id: int,
        following_id: int
    ) -> bool:
        """
        取消关注用户

        Args:
            db: 数据库会话
            follower_id: 关注者ID
            following_id: 被关注者ID

        Returns:
            是否取消成功
        """
        result = await db.execute(
            select(Follow)
            .where(
                and_(
                    Follow.follower_id == follower_id,
                    Follow.following_id == following_id
                )
            )
        )
        follow = result.scalar_one_or_none()

        if not follow:
            return False

        await db.delete(follow)
        await db.commit()
        return True

    async def get_followers(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[User]:
        """
        获取用户的粉丝列表

        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过数量
            limit: 限制数量

        Returns:
            粉丝用户列表
        """
        result = await db.execute(
            select(User)
            .join(Follow, Follow.follower_id == User.id)
            .where(Follow.following_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def get_following(
        self,
        db: AsyncSession,
        user_id: int,
        skip: int = 0,
        limit: int = 20
    ) -> List[User]:
        """
        获取用户关注的用户列表

        Args:
            db: 数据库会话
            user_id: 用户ID
            skip: 跳过数量
            limit: 限制数量

        Returns:
            关注的用户列表
        """
        result = await db.execute(
            select(User)
            .join(Follow, Follow.following_id == User.id)
            .where(Follow.follower_id == user_id)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    async def search_users(
        self,
        db: AsyncSession,
        query: str,
        skip: int = 0,
        limit: int = 20
    ) -> List[User]:
        """
        搜索用户

        Args:
            db: 数据库会话
            query: 搜索关键词
            skip: 跳过数量
            limit: 限制数量

        Returns:
            匹配的用户列表
        """
        search_filter = or_(
            User.username.contains(query),
            User.nickname.contains(query),
            User.bio.contains(query)
        )

        result = await db.execute(
            select(User)
            .where(search_filter)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()


# 创建服务实例
user_service = UserService()