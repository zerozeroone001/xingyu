#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""检查数据是否为简体中文"""

import asyncio
import sys
import io
from pathlib import Path
import re

# 设置标准输出为UTF-8编码（Windows兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from app.core.config import settings
from app.models.author import Author
from app.models.poetry import Poetry


# 常见繁体字示例
TRADITIONAL_CHARS = "詩爲關無學國門風長來說過這裡還時間問題東國來說會經過還沒時間東來說會經過還沒時間東來說會經過還沒時間東國來說會經過還沒時"


def has_traditional_chars(text: str) -> bool:
    """检查文本中是否包含繁体字"""
    if not text:
        return False
    for char in TRADITIONAL_CHARS:
        if char in text:
            return True
    return False


async def check_data():
    """检查数据"""

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
        print("🔍 检查数据是否为简体中文")
        print("=" * 70)

        # 检查5首随机诗词
        result = await session.execute(
            select(Poetry, Author.name)
            .outerjoin(Author, Poetry.author_id == Author.id)
            .limit(10)
        )

        poetries = result.all()

        print(f"\n抽样检查 {len(poetries)} 首诗词：\n")

        traditional_count = 0
        simplified_count = 0

        for idx, (poetry, author_name) in enumerate(poetries, 1):
            has_trad = has_traditional_chars(poetry.title + poetry.content)

            status = "❌ 繁体" if has_trad else "✅ 简体"
            if has_trad:
                traditional_count += 1
            else:
                simplified_count += 1

            print(f"{idx}. {status} - 《{poetry.title}》 - {author_name or '佚名'}")
            # 显示前2行
            lines = poetry.content.split('\n')[:2]
            for line in lines:
                print(f"   {line}")
            print()

        print("=" * 70)
        print(f"✅ 简体: {simplified_count} 首")
        print(f"❌ 繁体: {traditional_count} 首")
        print("=" * 70)

        if traditional_count == 0:
            print("\n🎉 全部为简体中文！")
        else:
            print(f"\n⚠️  发现 {traditional_count} 首诗词包含繁体字")

    await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check_data())
