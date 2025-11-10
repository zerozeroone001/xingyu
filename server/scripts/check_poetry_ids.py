#!/usr/bin/env python3
"""
检查数据库中的诗词ID
"""

import asyncio
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.models.poetry import Poetry


async def check_ids():
    """检查数据库中的诗词ID"""

    # 创建数据库引擎
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,
        pool_pre_ping=True,
    )

    # 创建会话工厂
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async with async_session() as session:
        try:
            # 查询所有诗词的ID
            stmt = select(Poetry.id, Poetry.title, Poetry.status).order_by(Poetry.id).limit(20)
            result = await session.execute(stmt)
            poetries = result.all()

            print(f"\n数据库中的诗词ID列表（前20条）：")
            print("=" * 80)
            print(f"{'ID':<25} {'标题':<30} {'状态':<10}")
            print("=" * 80)

            for id, title, status in poetries:
                status_text = "已发布" if status == 1 else "草稿" if status == 2 else "已删除"
                print(f"{id:<25} {title:<30} {status_text:<10}")

            print("\n" + "=" * 80)

            # 查询总数
            count_stmt = select(Poetry)
            result = await session.execute(count_stmt)
            total = len(result.scalars().all())
            print(f"诗词总数: {total}")

            # 查询特定ID是否存在
            target_id = 768595412145755100
            stmt = select(Poetry).where(Poetry.id == target_id)
            result = await session.execute(stmt)
            poetry = result.scalar_one_or_none()

            print(f"\nID {target_id} 是否存在: {'是' if poetry else '否'}")
            if poetry:
                print(f"  标题: {poetry.title}")
                print(f"  状态: {poetry.status}")

        except Exception as e:
            print(f"\n❌ 查询失败: {str(e)}")
            import traceback
            traceback.print_exc()
        finally:
            await engine.dispose()


if __name__ == "__main__":
    asyncio.run(check_ids())
