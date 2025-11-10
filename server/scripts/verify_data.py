#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""验证导入的诗词数据"""

import asyncio
import sys
import io
from pathlib import Path
import random

# 设置标准输出为UTF-8编码（Windows兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.models.author import Author
from app.models.poetry import Poetry


async def verify_data():
    """验证数据"""

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

    async with async_session() as session:
        print("=" * 70)
        print("📊 数据库统计信息")
        print("=" * 70)

        # 统计作者总数
        result = await session.execute(select(func.count(Author.id)))
        author_count = result.scalar()
        print(f"\n👥 作者总数: {author_count}")

        # 统计诗词总数
        result = await session.execute(select(func.count(Poetry.id)))
        poetry_count = result.scalar()
        print(f"📖 诗词总数: {poetry_count}")

        # 按类型统计
        print("\n📚 按类型统计:")
        for poem_type in ['绝句', '律诗', '古诗']:
            result = await session.execute(
                select(func.count(Poetry.id)).where(Poetry.type == poem_type)
            )
            count = result.scalar()
            percentage = (count / poetry_count * 100) if poetry_count > 0 else 0
            print(f"   {poem_type}: {count:,} 首 ({percentage:.1f}%)")

        # 随机展示5首诗
        print("\n" + "=" * 70)
        print("🎲 随机诗词展示")
        print("=" * 70)

        # 获取所有诗词ID
        result = await session.execute(select(Poetry.id))
        all_ids = [row[0] for row in result.all()]

        # 随机选择5个ID
        sample_ids = random.sample(all_ids, min(5, len(all_ids)))

        for idx, poetry_id in enumerate(sample_ids, 1):
            result = await session.execute(
                select(Poetry).where(Poetry.id == poetry_id)
            )
            poetry = result.scalar_one()

            # 获取作者信息
            author_name = "佚名"
            if poetry.author_id:
                result = await session.execute(
                    select(Author).where(Author.id == poetry.author_id)
                )
                author = result.scalar_one_or_none()
                if author:
                    author_name = author.name

            print(f"\n[{idx}] 《{poetry.title}》 - {author_name} ({poetry.dynasty})")
            print(f"    类型: {poetry.type or '未分类'}")

            # 显示前4行内容
            lines = poetry.content.split('\n')[:4]
            for line in lines:
                print(f"    {line}")
            if len(poetry.content.split('\n')) > 4:
                print(f"    ...")

        # 展示热门作者
        print("\n" + "=" * 70)
        print("⭐ 作品最多的作者 TOP 10")
        print("=" * 70)

        result = await session.execute(
            select(
                Author.name,
                Author.dynasty,
                func.count(Poetry.id).label('poetry_count')
            )
            .join(Poetry, Author.id == Poetry.author_id)
            .group_by(Author.id)
            .order_by(func.count(Poetry.id).desc())
            .limit(10)
        )

        top_authors = result.all()
        for idx, (name, dynasty, count) in enumerate(top_authors, 1):
            print(f"   {idx:2d}. {name} ({dynasty}) - {count:,} 首")

    await engine.dispose()
    print("\n✅ 验证完成！")


if __name__ == "__main__":
    asyncio.run(verify_data())
