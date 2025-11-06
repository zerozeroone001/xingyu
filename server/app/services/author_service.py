"""
作者服务层
"""

from typing import List, Optional, Tuple
from sqlalchemy import select, func, or_
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author import Author
from app.schemas.author import AuthorCreate, AuthorUpdate


class AuthorService:
    """作者服务"""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_list(
        self,
        keyword: Optional[str] = None,
        dynasty: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "id",
        order: str = "desc",
    ) -> Tuple[List[Author], int]:
        """
        获取作者列表

        Args:
            keyword: 关键词搜索（姓名、简介）
            dynasty: 朝代筛选
            page: 页码
            page_size: 每页数量
            sort_by: 排序字段
            order: 排序方式

        Returns:
            (作者列表, 总数)
        """
        # 构建查询
        query = select(Author)

        # 关键词搜索
        if keyword:
            query = query.where(
                or_(
                    Author.name.like(f"%{keyword}%"),
                    Author.intro.like(f"%{keyword}%"),
                )
            )

        # 朝代筛选
        if dynasty:
            query = query.where(Author.dynasty == dynasty)

        # 获取总数
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()

        # 排序
        sort_column = getattr(Author, sort_by, Author.id)
        if order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # 分页
        offset = (page - 1) * page_size
        query = query.offset(offset).limit(page_size)

        # 执行查询
        result = await self.db.execute(query)
        authors = result.scalars().all()

        return list(authors), total

    async def get_by_id(self, author_id: int) -> Optional[Author]:
        """
        根据ID获取作者

        Args:
            author_id: 作者ID

        Returns:
            作者对象
        """
        result = await self.db.execute(
            select(Author).where(Author.id == author_id)
        )
        return result.scalar_one_or_none()

    async def get_by_name(self, name: str) -> Optional[Author]:
        """
        根据姓名获取作者

        Args:
            name: 作者姓名

        Returns:
            作者对象
        """
        result = await self.db.execute(
            select(Author).where(Author.name == name)
        )
        return result.scalar_one_or_none()

    async def create(self, author_data: AuthorCreate) -> Author:
        """
        创建作者

        Args:
            author_data: 作者数据

        Returns:
            创建的作者对象
        """
        author = Author(**author_data.model_dump())
        self.db.add(author)
        await self.db.commit()
        await self.db.refresh(author)
        return author

    async def update(
        self, author_id: int, author_data: AuthorUpdate
    ) -> Optional[Author]:
        """
        更新作者

        Args:
            author_id: 作者ID
            author_data: 更新数据

        Returns:
            更新后的作者对象
        """
        author = await self.get_by_id(author_id)
        if not author:
            return None

        # 更新字段
        update_data = author_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(author, field, value)

        await self.db.commit()
        await self.db.refresh(author)
        return author

    async def delete(self, author_id: int) -> bool:
        """
        删除作者

        Args:
            author_id: 作者ID

        Returns:
            是否删除成功
        """
        author = await self.get_by_id(author_id)
        if not author:
            return False

        await self.db.delete(author)
        await self.db.commit()
        return True

    async def get_hot_authors(self, limit: int = 10) -> List[Author]:
        """
        获取热门作者（按诗词数量排序）

        Args:
            limit: 数量限制

        Returns:
            作者列表
        """
        # 这里可以通过关联poetries表统计，暂时简化处理
        query = (
            select(Author)
            .order_by(Author.id.desc())
            .limit(limit)
        )

        result = await self.db.execute(query)
        authors = result.scalars().all()
        return list(authors)

    async def search_by_dynasty(self, dynasty: str) -> List[Author]:
        """
        按朝代搜索作者

        Args:
            dynasty: 朝代

        Returns:
            作者列表
        """
        result = await self.db.execute(
            select(Author).where(Author.dynasty == dynasty).order_by(Author.id)
        )
        authors = result.scalars().all()
        return list(authors)
