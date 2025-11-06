"""
消息服务层
"""

from typing import List, Optional, Tuple, Dict, Any
from datetime import datetime
from sqlalchemy import select, func, and_, desc, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.models.message import Message
from app.schemas.message import MessageCreate


class MessageService:
    """消息服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        user_id: int,
        type_: Optional[str] = None,
        is_read: Optional[int] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> Tuple[List[Message], int]:
        """
        获取用户消息列表

        Args:
            user_id: 用户ID
            type_: 消息类型筛选
            is_read: 读取状态筛选
            page: 页码
            page_size: 每页数量

        Returns:
            (消息列表, 总数)
        """
        # 构建查询条件
        conditions = [Message.user_id == user_id]

        if type_:
            conditions.append(Message.type == type_)

        if is_read is not None:
            conditions.append(Message.is_read == is_read)

        # 计算总数
        count_query = select(func.count(Message.id)).where(and_(*conditions))
        count_result = await self.db.execute(count_query)
        total = count_result.scalar() or 0

        # 查询消息列表
        query = (
            select(Message)
            .options(joinedload(Message.from_user))
            .where(and_(*conditions))
            .order_by(desc(Message.created_at))
            .offset((page - 1) * page_size)
            .limit(page_size)
        )

        result = await self.db.execute(query)
        messages = result.unique().scalars().all()

        return list(messages), total

    async def get_by_id(self, message_id: int, user_id: int) -> Optional[Message]:
        """
        获取消息详情

        Args:
            message_id: 消息ID
            user_id: 用户ID（权限验证）

        Returns:
            消息对象
        """
        query = (
            select(Message)
            .options(joinedload(Message.from_user))
            .where(and_(Message.id == message_id, Message.user_id == user_id))
        )

        result = await self.db.execute(query)
        return result.unique().scalar_one_or_none()

    async def create(self, message_data: MessageCreate) -> Message:
        """
        创建消息

        Args:
            message_data: 消息数据

        Returns:
            创建的消息对象
        """
        message = Message(
            user_id=message_data.user_id,
            type=message_data.type,
            title=message_data.title,
            content=message_data.content,
            data=message_data.data,
            from_user_id=message_data.from_user_id,
            target_type=message_data.target_type,
            target_id=message_data.target_id,
            is_read=0,
        )

        self.db.add(message)
        await self.db.commit()
        await self.db.refresh(message)

        return message

    async def mark_as_read(self, message_id: int, user_id: int) -> bool:
        """
        标记消息为已读

        Args:
            message_id: 消息ID
            user_id: 用户ID（权限验证）

        Returns:
            是否成功
        """
        message = await self.get_by_id(message_id, user_id)
        if not message:
            return False

        if message.is_read == 0:
            message.is_read = 1
            message.read_at = datetime.utcnow()
            await self.db.commit()

        return True

    async def mark_all_as_read(self, user_id: int, type_: Optional[str] = None) -> int:
        """
        标记所有消息为已读

        Args:
            user_id: 用户ID
            type_: 消息类型（可选，为空则标记全部）

        Returns:
            标记数量
        """
        conditions = [Message.user_id == user_id, Message.is_read == 0]

        if type_:
            conditions.append(Message.type == type_)

        stmt = (
            update(Message)
            .where(and_(*conditions))
            .values(is_read=1, read_at=datetime.utcnow())
        )

        result = await self.db.execute(stmt)
        await self.db.commit()

        return result.rowcount

    async def delete(self, message_id: int, user_id: int) -> bool:
        """
        删除消息

        Args:
            message_id: 消息ID
            user_id: 用户ID（权限验证）

        Returns:
            是否成功
        """
        message = await self.get_by_id(message_id, user_id)
        if not message:
            return False

        await self.db.delete(message)
        await self.db.commit()

        return True

    async def get_unread_count(self, user_id: int) -> int:
        """
        获取未读消息数

        Args:
            user_id: 用户ID

        Returns:
            未读消息数
        """
        query = select(func.count(Message.id)).where(
            and_(Message.user_id == user_id, Message.is_read == 0)
        )

        result = await self.db.execute(query)
        return result.scalar() or 0

    async def get_stats(self, user_id: int) -> Dict[str, int]:
        """
        获取消息统计

        Args:
            user_id: 用户ID

        Returns:
            统计数据
        """
        # 总消息数
        total_query = select(func.count(Message.id)).where(Message.user_id == user_id)
        total_result = await self.db.execute(total_query)
        total = total_result.scalar() or 0

        # 未读消息数
        unread_query = select(func.count(Message.id)).where(
            and_(Message.user_id == user_id, Message.is_read == 0)
        )
        unread_result = await self.db.execute(unread_query)
        unread = unread_result.scalar() or 0

        # 各类型消息数
        type_query = (
            select(Message.type, func.count(Message.id))
            .where(and_(Message.user_id == user_id, Message.is_read == 0))
            .group_by(Message.type)
        )
        type_result = await self.db.execute(type_query)
        type_counts = {row[0]: row[1] for row in type_result.all()}

        return {
            "total": total,
            "unread": unread,
            "system": type_counts.get("system", 0),
            "like": type_counts.get("like", 0),
            "comment": type_counts.get("comment", 0),
            "follow": type_counts.get("follow", 0),
            "collect": type_counts.get("collect", 0),
        }

    async def create_like_message(
        self,
        user_id: int,
        from_user_id: int,
        target_type: str,
        target_id: int,
        target_title: str,
    ) -> Message:
        """
        创建点赞消息

        Args:
            user_id: 接收用户ID
            from_user_id: 点赞用户ID
            target_type: 目标类型（poetry/post）
            target_id: 目标ID
            target_title: 目标标题

        Returns:
            消息对象
        """
        # 避免给自己发消息
        if user_id == from_user_id:
            return None

        message_data = MessageCreate(
            user_id=user_id,
            from_user_id=from_user_id,
            type="like",
            title="收到新的点赞",
            content=f"赞了你的{target_title}",
            target_type=target_type,
            target_id=target_id,
        )

        return await self.create(message_data)

    async def create_comment_message(
        self,
        user_id: int,
        from_user_id: int,
        target_type: str,
        target_id: int,
        comment_content: str,
    ) -> Message:
        """
        创建评论消息

        Args:
            user_id: 接收用户ID
            from_user_id: 评论用户ID
            target_type: 目标类型（poetry/post）
            target_id: 目标ID
            comment_content: 评论内容

        Returns:
            消息对象
        """
        # 避免给自己发消息
        if user_id == from_user_id:
            return None

        # 截取评论内容前50字
        content_preview = (
            comment_content[:50] + "..." if len(comment_content) > 50 else comment_content
        )

        message_data = MessageCreate(
            user_id=user_id,
            from_user_id=from_user_id,
            type="comment",
            title="收到新的评论",
            content=content_preview,
            target_type=target_type,
            target_id=target_id,
        )

        return await self.create(message_data)

    async def create_follow_message(
        self, user_id: int, from_user_id: int
    ) -> Message:
        """
        创建关注消息

        Args:
            user_id: 被关注用户ID
            from_user_id: 关注用户ID

        Returns:
            消息对象
        """
        # 避免给自己发消息
        if user_id == from_user_id:
            return None

        message_data = MessageCreate(
            user_id=user_id,
            from_user_id=from_user_id,
            type="follow",
            title="新的关注",
            content="关注了你",
        )

        return await self.create(message_data)

    async def create_collect_message(
        self,
        user_id: int,
        from_user_id: int,
        target_type: str,
        target_id: int,
        target_title: str,
    ) -> Message:
        """
        创建收藏消息

        Args:
            user_id: 接收用户ID
            from_user_id: 收藏用户ID
            target_type: 目标类型（poetry/post）
            target_id: 目标ID
            target_title: 目标标题

        Returns:
            消息对象
        """
        # 避免给自己发消息
        if user_id == from_user_id:
            return None

        message_data = MessageCreate(
            user_id=user_id,
            from_user_id=from_user_id,
            type="collect",
            title="收到新的收藏",
            content=f"收藏了你的{target_title}",
            target_type=target_type,
            target_id=target_id,
        )

        return await self.create(message_data)

    async def create_system_message(
        self, user_id: int, title: str, content: str
    ) -> Message:
        """
        创建系统消息

        Args:
            user_id: 接收用户ID
            title: 消息标题
            content: 消息内容

        Returns:
            消息对象
        """
        message_data = MessageCreate(
            user_id=user_id,
            type="system",
            title=title,
            content=content,
        )

        return await self.create(message_data)
