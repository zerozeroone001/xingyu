#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
将诗词数据同步到 Elasticsearch
"""

import asyncio
import sys
import io
from pathlib import Path

# 设置标准输出为UTF-8编码（Windows兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from elasticsearch import Elasticsearch, helpers

from app.core.config import settings
from app.models.author import Author
from app.models.poetry import Poetry


async def sync_to_es(batch_size: int = 1000):
    """同步数据到 Elasticsearch"""

    # 连接数据库
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # 连接 Elasticsearch
    es = Elasticsearch([settings.ELASTICSEARCH_URL])

    print("=" * 70)
    print("🔄 同步诗词数据到 Elasticsearch")
    print("=" * 70)

    # 检查索引是否存在
    index_name = "poetry_index"

    if es.indices.exists(index=index_name):
        print(f"\n⚠️  索引 {index_name} 已存在")
        response = input("是否删除现有索引并重新创建? (y/n): ")
        if response.lower() == 'y':
            es.indices.delete(index=index_name)
            print(f"✅ 已删除索引 {index_name}")
        else:
            print("⏭️  跳过索引创建")

    # 创建索引
    if not es.indices.exists(index=index_name):
        print(f"\n📝 创建索引 {index_name}...")

        index_body = {
            "settings": {
                "number_of_shards": 1,
                "number_of_replicas": 0,
                "analysis": {
                    "analyzer": {
                        "ik_analyzer": {
                            "type": "standard"
                        }
                    }
                }
            },
            "mappings": {
                "properties": {
                    "id": {"type": "long"},
                    "title": {"type": "text"},
                    "content": {"type": "text"},
                    "author_name": {"type": "text"},
                    "author_id": {"type": "long"},
                    "dynasty": {"type": "keyword"},
                    "type": {"type": "keyword"},
                    "tags": {"type": "keyword"}
                }
            }
        }

        es.indices.create(index=index_name, body=index_body)
        print(f"✅ 索引创建成功")

    # 获取所有诗词
    async with async_session() as session:
        print(f"\n📖 读取诗词数据...")

        result = await session.execute(
            select(Poetry, Author.name)
            .outerjoin(Author, Poetry.author_id == Author.id)
        )

        poetries = result.all()
        total = len(poetries)

        print(f"✅ 共读取 {total:,} 首诗词")

        # 准备批量插入数据
        print(f"\n🔄 开始同步到 Elasticsearch (批次大小: {batch_size})...")

        actions = []
        synced = 0

        for poetry, author_name in poetries:
            doc = {
                "_index": index_name,
                "_id": str(poetry.id),
                "_source": {
                    "id": poetry.id,
                    "title": poetry.title,
                    "content": poetry.content,
                    "author_name": author_name or "佚名",
                    "author_id": poetry.author_id,
                    "dynasty": poetry.dynasty,
                    "type": poetry.type,
                    "tags": poetry.tags or []
                }
            }

            actions.append(doc)

            # 每达到批次大小就执行一次批量插入
            if len(actions) >= batch_size:
                helpers.bulk(es, actions)
                synced += len(actions)
                print(f"   已同步 {synced:,} / {total:,} ({synced/total*100:.1f}%)")
                actions = []

        # 插入剩余数据
        if actions:
            helpers.bulk(es, actions)
            synced += len(actions)
            print(f"   已同步 {synced:,} / {total:,} ({synced/total*100:.1f}%)")

    # 刷新索引
    es.indices.refresh(index=index_name)

    # 验证数据
    count = es.count(index=index_name)['count']
    print(f"\n✅ 同步完成！")
    print(f"   Elasticsearch 中的文档数: {count:,}")

    # 测试搜索
    print(f"\n🔍 测试搜索...")
    search_result = es.search(
        index=index_name,
        body={
            "query": {
                "multi_match": {
                    "query": "春眠",
                    "fields": ["title", "content", "author_name"]
                }
            },
            "size": 3
        }
    )

    hits = search_result['hits']['hits']
    print(f"   搜索 '春眠' 找到 {search_result['hits']['total']['value']} 个结果")

    if hits:
        print(f"\n   前3个结果:")
        for idx, hit in enumerate(hits, 1):
            source = hit['_source']
            print(f"   {idx}. 《{source['title']}》 - {source['author_name']}")

    await engine.dispose()
    print(f"\n✅ 全部完成！")


if __name__ == "__main__":
    print("=" * 70)
    print("🚀 星语诗词平台 - Elasticsearch 同步工具")
    print("=" * 70)
    print()

    try:
        asyncio.run(sync_to_es())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断同步")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 同步过程出错: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
