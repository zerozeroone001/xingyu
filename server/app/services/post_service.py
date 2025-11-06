"""
广场内容服务层
"""

from typing import List, Optional, Tuple
from datetime import datetime
from sqlalchemy import select, func, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.post import Post
from app.models.user import User
from app.models.poetry import Poetry
from app.schemas.post import PostCreate, PostUpdate


class PostService:
    """广场内容服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        type_: Optional[str] = None,
        user_id: Optional[int] = None,
        tag: Optional[str] = None,
        status: int = 1,
        page: int = 1,
        page_size: int = 20,
        order_by: str = "created_at",
    ) -> Tuple[List[Post], int]:
        """
        获取广场内容列表

        Args:
            type_: 类型筛选
            user_id: 用户ID筛选
            tag: 标签筛选
            status: 状态筛选
            page: 页码
            page_size: 每页数量
            order_by: 排序字段

        Returns:
            (内容列表, 总数)
        """
        # 构建查询条件
        conditions = [Post.status == status]

        if type_:
            conditions.append(Post.type == type_)

        if user_id:
            conditions.append(Post.user_id == user_id)

        if tag:
            # JSON字段包含查询
            conditions.append(func.json_contains(Post.tags, f'"{tag}"'))

        # 计算总数
        count_query = select(func.count(Post.id)).where(and_(*conditions))
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # 构建查询
        query = (
            select(Post)
            .options(
                joinedload(Post.user),
                joinedload(Post.poetry),
            )
            .where(and_(*conditions))
        )

        # 排序
        if order_by == "like_count":
            query = query.order_by(desc(Post.like_count))
        elif order_by == "view_count":
            query = query.order_by(desc(Post.view_count))
        else:
            query = query.order_by(desc(Post.created_at))

        # 分页
        query = query.offset((page - 1) * page_size).limit(page_size)

        result = await self.db.execute(query)
        posts = result.unique().scalars().all()

        return list(posts), total

    async def get_by_id(self, post_id: int) -> Optional[Post]:
        """
        根据ID获取广场内容详情

        Args:
            post_id: 内容ID

        Returns:
            内容对象
        """
        query = (
            select(Post)
            .options(
                joinedload(Post.user),
                joinedload(Post.poetry),
            )
            .where(Post.id == post_id)
        )

        result = await self.db.execute(query)
        return result.unique().scalar_one_or_none()

    async def create(self, user_id: int, post_data: PostCreate) -> Post:
        """
        创建广场内容

        Args:
            user_id: 用户ID
            post_data: 内容数据

        Returns:
            创建的内容对象
        """
        # 如果是分享类型，验证诗词是否存在
        if post_data.type == "share" and post_data.poetry_id:
            poetry = await self.db.get(Poetry, post_data.poetry_id)
            if not poetry:
                raise ValueError("关联的诗词不存在")

        post = Post(
            user_id=user_id,
            content=post_data.content,
            images=post_data.images,
            tags=post_data.tags,
            poetry_id=post_data.poetry_id,
            type=post_data.type,
            status=1,  # 默认已发布
        )

        self.db.add(post)
        await self.db.commit()
        await self.db.refresh(post)

        # 加载关联数据
        await self.db.refresh(post, ["user", "poetry"])

        return post

    async def update(
        self, post_id: int, user_id: int, post_data: PostUpdate
    ) -> Optional[Post]:
        """
        更新广场内容

        Args:
            post_id: 内容ID
            user_id: 用户ID（权限验证）
            post_data: 更新数据

        Returns:
            更新后的内容对象
        """
        post = await self.db.get(Post, post_id)
        if not post:
            return None

        # 验证权限
        if post.user_id != user_id:
            raise PermissionError("无权修改此内容")

        # 更新字段
        update_data = post_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(post, field, value)

        await self.db.commit()
        await self.db.refresh(post)

        # 加载关联数据
        await self.db.refresh(post, ["user", "poetry"])

        return post

    async def delete(self, post_id: int, user_id: int) -> bool:
        """
        删除广场内容（软删除）

        Args:
            post_id: 内容ID
            user_id: 用户ID（权限验证）

        Returns:
            是否成功
        """
        post = await self.db.get(Post, post_id)
        if not post:
            return False

        # 验证权限
        if post.user_id != user_id:
            raise PermissionError("无权删除此内容")

        # 软删除
        post.status = 3
        await self.db.commit()

        return True

    async def increment_view_count(self, post_id: int) -> bool:
        """
        增加浏览数

        Args:
            post_id: 内容ID

        Returns:
            是否成功
        """
        post = await self.db.get(Post, post_id)
        if not post:
            return False

        post.view_count += 1
        await self.db.commit()

        return True

    async def increment_like_count(self, post_id: int) -> bool:
        """
        增加点赞数

        Args:
            post_id: 内容ID

        Returns:
            是否成功
        """
        post = await self.db.get(Post, post_id)
        if not post:
            return False

        post.like_count += 1
        await self.db.commit()

        return True

    async def decrement_like_count(self, post_id: int) -> bool:
        """
        减少点赞数

        Args:
            post_id: 内容ID

        Returns:
            是否成功
        """
        post = await self.db.get(Post, post_id)
        if not post:
            return False

        post.like_count = max(0, post.like_count - 1)
        await self.db.commit()

        return True

    async def increment_comment_count(self, post_id: int) -> bool:
        """
        增加评论数

        Args:
            post_id: 内容ID

        Returns:
            是否成功
        """
        post = await self.db.get(Post, post_id)
        if not post:
            return False

        post.comment_count += 1
        await self.db.commit()

        return True

    async def decrement_comment_count(self, post_id: int) -> bool:
        """
        减少评论数

        Args:
            post_id: 内容ID

        Returns:
            是否成功
        """
        post = await self.db.get(Post, post_id)
        if not post:
            return False

        post.comment_count = max(0, post.comment_count - 1)
        await self.db.commit()

        return True

    async def get_following_posts(
        self, user_id: int, page: int = 1, page_size: int = 20
    ) -> Tuple[List[Post], int]:
        """
        获取关注用户的动态

        Args:
            user_id: 当前用户ID
            page: 页码
            page_size: 每页数量

        Returns:
            (内容列表, 总数)
        """
        from app.models.follow import Follow

        # 获取关注的用户ID列表
        following_query = select(Follow.follow_user_id).where(
            Follow.user_id == user_id
        )
        following_result = await self.db.execute(following_query)
        following_ids = [row[0] for row in following_result.all()]

        if not following_ids:
            return [], 0

        # 计算总数
        count_query = select(func.count(Post.id)).where(
            and_(Post.user_id.in_(following_ids), Post.status == 1)
        )
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # 查询动态
        query = (
            select(Post)
            .options(
                joinedload(Post.user),
                joinedload(Post.poetry),
            )
            .where(and_(Post.user_id.in_(following_ids), Post.status == 1))
            .order_by(desc(Post.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.db.execute(query)
        posts = result.unique().scalars().all()

        return list(posts), total
