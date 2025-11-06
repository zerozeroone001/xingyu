"""
Elasticsearch 客户端工具
"""

from typing import Optional
from elasticsearch import AsyncElasticsearch
from app.core.config import settings


class ESClient:
    """Elasticsearch客户端单例"""

    _instance: Optional[AsyncElasticsearch] = None

    @classmethod
    def get_client(cls) -> AsyncElasticsearch:
        """获取ES客户端实例"""
        if cls._instance is None:
            cls._instance = AsyncElasticsearch(
                hosts=[settings.ELASTICSEARCH_URL],
                # 如果ES需要认证，添加以下配置
                # basic_auth=("username", "password"),
            )
        return cls._instance

    @classmethod
    async def close(cls):
        """关闭ES客户端"""
        if cls._instance is not None:
            await cls._instance.close()
            cls._instance = None


# 创建全局实例
async def get_es_client() -> AsyncElasticsearch:
    """依赖注入函数"""
    return ESClient.get_client()
