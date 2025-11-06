"""
搜索服务层
"""

from typing import List, Dict, Any, Optional
from elasticsearch import AsyncElasticsearch
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload

from app.models.poetry import Poetry
from app.models.author import Author


class SearchService:
    """搜索服务"""

    # ES索引名称
    POETRY_INDEX = "poetries"

    def __init__(self, db: AsyncSession, es_client: AsyncElasticsearch):
        self.db = db
        self.es = es_client

    async def ensure_index(self):
        """确保索引存在，不存在则创建"""
        if not await self.es.indices.exists(index=self.POETRY_INDEX):
            await self.create_poetry_index()

    async def create_poetry_index(self):
        """创建诗词索引"""
        mappings = {
            "properties": {
                "id": {"type": "long"},
                "title": {
                    "type": "text",
                    "analyzer": "standard",
                    "fields": {"keyword": {"type": "keyword"}},
                },
                "content": {"type": "text", "analyzer": "standard"},
                "author_id": {"type": "long"},
                "author_name": {
                    "type": "text",
                    "analyzer": "standard",
                    "fields": {"keyword": {"type": "keyword"}},
                },
                "dynasty": {"type": "keyword"},
                "type": {"type": "keyword"},
                "tags": {"type": "keyword"},
                "read_count": {"type": "integer"},
                "like_count": {"type": "integer"},
                "collect_count": {"type": "integer"},
                "status": {"type": "integer"},
                "created_at": {"type": "date"},
                "updated_at": {"type": "date"},
            }
        }

        settings_config = {
            "number_of_shards": 1,
            "number_of_replicas": 0,
        }

        await self.es.indices.create(
            index=self.POETRY_INDEX, mappings=mappings, settings=settings_config
        )

    async def index_poetry(self, poetry: Poetry):
        """
        索引单个诗词

        Args:
            poetry: 诗词对象
        """
        await self.ensure_index()

        # 加载作者信息
        if poetry.author_id and not poetry.author:
            result = await self.db.execute(
                select(Poetry)
                .options(joinedload(Poetry.author))
                .where(Poetry.id == poetry.id)
            )
            poetry = result.scalar_one_or_none()

        doc = {
            "id": poetry.id,
            "title": poetry.title,
            "content": poetry.content,
            "author_id": poetry.author_id,
            "author_name": poetry.author.name if poetry.author else None,
            "dynasty": poetry.dynasty,
            "type": poetry.type,
            "tags": poetry.tags if poetry.tags else [],
            "read_count": poetry.read_count or 0,
            "like_count": poetry.like_count or 0,
            "collect_count": poetry.collect_count or 0,
            "status": poetry.status,
            "created_at": poetry.created_at,
            "updated_at": poetry.updated_at,
        }

        await self.es.index(index=self.POETRY_INDEX, id=poetry.id, document=doc)

    async def delete_poetry(self, poetry_id: int):
        """
        从索引中删除诗词

        Args:
            poetry_id: 诗词ID
        """
        try:
            await self.es.delete(index=self.POETRY_INDEX, id=poetry_id)
        except Exception:
            # 如果文档不存在，忽略错误
            pass

    async def search_poetries(
        self,
        keyword: Optional[str] = None,
        dynasty: Optional[str] = None,
        type_: Optional[str] = None,
        tags: Optional[List[str]] = None,
        author_name: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
        sort_by: str = "_score",
        order: str = "desc",
    ) -> Dict[str, Any]:
        """
        搜索诗词

        Args:
            keyword: 关键词（搜索标题和内容）
            dynasty: 朝代
            type_: 类型
            tags: 标签列表
            author_name: 作者名称
            page: 页码
            page_size: 每页数量
            sort_by: 排序字段
            order: 排序方式

        Returns:
            搜索结果
        """
        await self.ensure_index()

        # 构建查询
        must_queries = []
        should_queries = []
        filter_queries = []

        # 关键词搜索
        if keyword:
            should_queries.append(
                {"match": {"title": {"query": keyword, "boost": 2.0}}}
            )
            should_queries.append({"match": {"content": {"query": keyword}}})
            should_queries.append({"match": {"author_name": {"query": keyword}}})

        # 筛选条件
        filter_queries.append({"term": {"status": 1}})  # 只搜索已发布的

        if dynasty:
            filter_queries.append({"term": {"dynasty": dynasty}})

        if type_:
            filter_queries.append({"term": {"type": type_}})

        if tags:
            for tag in tags:
                filter_queries.append({"term": {"tags": tag}})

        if author_name:
            filter_queries.append({"match": {"author_name": author_name}})

        # 构建bool查询
        query = {"bool": {}}

        if must_queries:
            query["bool"]["must"] = must_queries

        if should_queries:
            query["bool"]["should"] = should_queries
            query["bool"]["minimum_should_match"] = 1

        if filter_queries:
            query["bool"]["filter"] = filter_queries

        # 如果没有任何条件，查询所有
        if not must_queries and not should_queries:
            query = {"match_all": {}}
            if filter_queries:
                query = {"bool": {"filter": filter_queries}}

        # 排序
        sort = []
        if sort_by == "_score":
            sort.append({"_score": {"order": order}})
        else:
            sort.append({sort_by: {"order": order}})
            sort.append("_score")  # 次要按相关度排序

        # 计算分页
        from_ = (page - 1) * page_size

        # 执行搜索
        response = await self.es.search(
            index=self.POETRY_INDEX,
            query=query,
            sort=sort,
            from_=from_,
            size=page_size,
        )

        # 提取结果
        hits = response["hits"]
        total = hits["total"]["value"]
        items = [hit["_source"] for hit in hits["hits"]]

        return {
            "items": items,
            "total": total,
            "page": page,
            "page_size": page_size,
            "total_pages": (total + page_size - 1) // page_size,
        }

    async def bulk_index_poetries(self, batch_size: int = 100):
        """
        批量索引所有诗词

        Args:
            batch_size: 批量大小
        """
        await self.ensure_index()

        # 查询所有已发布的诗词
        result = await self.db.execute(
            select(Poetry)
            .options(joinedload(Poetry.author))
            .where(Poetry.status == 1)
        )
        poetries = result.scalars().all()

        # 批量索引
        bulk_data = []
        for poetry in poetries:
            # 索引操作
            bulk_data.append({"index": {"_index": self.POETRY_INDEX, "_id": poetry.id}})

            # 文档数据
            doc = {
                "id": poetry.id,
                "title": poetry.title,
                "content": poetry.content,
                "author_id": poetry.author_id,
                "author_name": poetry.author.name if poetry.author else None,
                "dynasty": poetry.dynasty,
                "type": poetry.type,
                "tags": poetry.tags if poetry.tags else [],
                "read_count": poetry.read_count or 0,
                "like_count": poetry.like_count or 0,
                "collect_count": poetry.collect_count or 0,
                "status": poetry.status,
                "created_at": poetry.created_at,
                "updated_at": poetry.updated_at,
            }
            bulk_data.append(doc)

            # 达到批量大小，执行索引
            if len(bulk_data) >= batch_size * 2:
                await self.es.bulk(operations=bulk_data)
                bulk_data = []

        # 索引剩余数据
        if bulk_data:
            await self.es.bulk(operations=bulk_data)

    async def suggest(self, prefix: str, size: int = 10) -> List[str]:
        """
        搜索建议

        Args:
            prefix: 前缀
            size: 返回数量

        Returns:
            建议列表
        """
        await self.ensure_index()

        query = {
            "bool": {
                "should": [
                    {"prefix": {"title.keyword": prefix}},
                    {"prefix": {"author_name.keyword": prefix}},
                ],
                "filter": [{"term": {"status": 1}}],
            }
        }

        response = await self.es.search(
            index=self.POETRY_INDEX,
            query=query,
            _source=["title", "author_name"],
            size=size,
        )

        # 提取建议
        suggestions = []
        for hit in response["hits"]["hits"]:
            source = hit["_source"]
            if source.get("title"):
                suggestions.append(source["title"])
            if source.get("author_name"):
                suggestions.append(source["author_name"])

        # 去重并返回
        return list(set(suggestions))[:size]
