"""
评论服务层
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func, and_, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.comment import Comment
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentUpdate


class CommentService:
    """评论服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        target_type: str,
        target_id: int,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "created_at",
        order: str = "desc",
        parent_id: Optional[int] = None,
    ) -> Tuple[List[Comment], int]:
        """
        获取评论列表

        Args:
            target_type: 目标类型
            target_id: 目标ID
            page: 页码
            page_size: 每页数量
            sort_by: 排序字段
            order: 排序方式
            parent_id: 父评论ID（None=一级评论）

        Returns:
            (评论列表, 总数)
        """
        # 构建查询
        query = (
            select(Comment)
            .options(joinedload(Comment.user))
            .where(
                and_(
                    Comment.target_type == target_type,
                    Comment.target_id == target_id,
                    Comment.status == 1,  # 只查询正常状态的评论
                )
            )
        )

        # 过滤父评论ID
        if parent_id is None:
            query = query.where(Comment.parent_id.is_(None))
        else:
            query = query.where(Comment.parent_id == parent_id)

        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 排序
        sort_column = getattr(Comment, sort_by, Comment.created_at)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        comments = result.scalars().all()

        return list(comments), total

    async def get_by_id(self, comment_id: int) -> Optional[Comment]:
        """
        根据ID获取评论

        Args:
            comment_id: 评论ID

        Returns:
            评论对象
        """
        result = await self.db.execute(
            select(Comment)
            .options(joinedload(Comment.user))
            .where(Comment.id == comment_id)
        )
        return result.scalar_one_or_none()

    async def create(self, user_id: int, comment_data: CommentCreate) -> Comment:
        """
        创建评论

        Args:
            user_id: 用户ID
            comment_data: 评论数据

        Returns:
            创建的评论对象
        """
        # 如果是二级评论，增加父评论的回复数
        if comment_data.parent_id:
            await self.db.execute(
                update(Comment)
                .where(Comment.id == comment_data.parent_id)
                .values(reply_count=Comment.reply_count + 1)
            )

        # 创建评论
        comment = Comment(
            user_id=user_id,
            target_type=comment_data.target_type,
            target_id=comment_data.target_id,
            parent_id=comment_data.parent_id,
            content=comment_data.content,
        )

        self.db.add(comment)
        await self.db.commit()
        await self.db.refresh(comment)

        # 加载用户信息
        result = await self.db.execute(
            select(Comment)
            .options(joinedload(Comment.user))
            .where(Comment.id == comment.id)
        )
        return result.scalar_one()

    async def update(
        self, comment_id: int, user_id: int, comment_data: CommentUpdate
    ) -> Optional[Comment]:
        """
        更新评论

        Args:
            comment_id: 评论ID
            user_id: 用户ID（权限检查）
            comment_data: 更新数据

        Returns:
            更新后的评论对象
        """
        comment = await self.get_by_id(comment_id)
        if not comment or comment.user_id != user_id:
            return None

        # 更新内容
        comment.content = comment_data.content

        await self.db.commit()
        await self.db.refresh(comment)
        return comment

    async def delete(self, comment_id: int, user_id: int) -> bool:
        """
        删除评论（软删除）

        Args:
            comment_id: 评论ID
            user_id: 用户ID（权限检查）

        Returns:
            是否删除成功
        """
        comment = await self.get_by_id(comment_id)
        if not comment or comment.user_id != user_id:
            return False

        # 软删除
        comment.status = 2

        # 如果是二级评论，减少父评论的回复数
        if comment.parent_id:
            await self.db.execute(
                update(Comment)
                .where(Comment.id == comment.parent_id)
                .values(reply_count=func.greatest(Comment.reply_count - 1, 0))
            )

        await self.db.commit()
        return True

    async def get_replies(
        self, parent_id: int, page: int = 1, page_size: int = 10
    ) -> Tuple[List[Comment], int]:
        """
        获取评论的回复列表

        Args:
            parent_id: 父评论ID
            page: 页码
            page_size: 每页数量

        Returns:
            (回复列表, 总数)
        """
        query = (
            select(Comment)
            .options(joinedload(Comment.user))
            .where(
                and_(
                    Comment.parent_id == parent_id,
                    Comment.status == 1,
                )
            )
            .order_by(Comment.created_at.asc())
        )

        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        replies = result.scalars().all()

        return list(replies), total

    async def get_user_comments(
        self, user_id: int, page: int = 1, page_size: int = 20
    ) -> Tuple[List[Comment], int]:
        """
        获取用户的评论列表

        Args:
            user_id: 用户ID
            page: 页码
            page_size: 每页数量

        Returns:
            (评论列表, 总数)
        """
        query = (
            select(Comment)
            .options(joinedload(Comment.user))
            .where(
                and_(
                    Comment.user_id == user_id,
                    Comment.status == 1,
                )
            )
            .order_by(Comment.created_at.desc())
        )

        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        comments = result.scalars().all()

        return list(comments), total

    async def increment_like_count(self, comment_id: int) -> bool:
        """
        增加评论点赞数

        Args:
            comment_id: 评论ID

        Returns:
            是否成功
        """
        comment = await self.get_by_id(comment_id)
        if not comment:
            return False

        comment.like_count = (comment.like_count or 0) + 1
        await self.db.commit()
        return True

    async def decrement_like_count(self, comment_id: int) -> bool:
        """
        减少评论点赞数

        Args:
            comment_id: 评论ID

        Returns:
            是否成功
        """
        comment = await self.get_by_id(comment_id)
        if not comment or comment.like_count <= 0:
            return False

        comment.like_count -= 1
        await self.db.commit()
        return True
