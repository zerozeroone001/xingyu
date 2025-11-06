#!/usr/bin/env python3
"""
诗词数据导入脚本

从sample_data.json导入作者和诗词数据到数据库
"""

import asyncio
import json
import sys
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.core.config import settings
from app.models.author import Author
from app.models.poetry import Poetry


async def import_data():
    """导入数据"""

    # 创建数据库引擎
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=True,
        pool_pre_ping=True,
    )

    # 创建会话工厂
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    # 读取JSON数据
    script_dir = Path(__file__).parent
    data_file = script_dir / "sample_data.json"

    print(f"📖 正在读取数据文件: {data_file}")

    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    print(f"✅ 数据文件读取成功")
    print(f"   - 作者数量: {len(data['authors'])}")
    print(f"   - 诗词数量: {len(data['poetries'])}")

    async with async_session() as session:
        try:
            # 导入作者数据
            print("\n📝 开始导入作者数据...")
            authors_imported = 0

            for author_data in data["authors"]:
                # 检查作者是否已存在
                result = await session.execute(
                    select(Author).where(Author.id == author_data["id"])
                )
                existing_author = result.scalar_one_or_none()

                if existing_author:
                    print(f"   ⏭️  作者已存在，跳过: {author_data['name']}")
                    continue

                # 创建作者
                author = Author(
                    id=author_data["id"],
                    name=author_data["name"],
                    dynasty=author_data["dynasty"],
                    intro=author_data.get("intro"),
                    birth_year=author_data.get("birth_year"),
                    death_year=author_data.get("death_year"),
                )

                session.add(author)
                authors_imported += 1
                print(f"   ✅ 导入作者: {author_data['name']} ({author_data['dynasty']})")

            await session.commit()
            print(f"\n✅ 作者数据导入完成，成功导入 {authors_imported} 位作者")

            # 导入诗词数据
            print("\n📝 开始导入诗词数据...")
            poetries_imported = 0

            for poetry_data in data["poetries"]:
                # 检查诗词是否已存在
                result = await session.execute(
                    select(Poetry).where(Poetry.id == poetry_data["id"])
                )
                existing_poetry = result.scalar_one_or_none()

                if existing_poetry:
                    print(f"   ⏭️  诗词已存在，跳过: {poetry_data['title']}")
                    continue

                # 创建诗词
                poetry = Poetry(
                    id=poetry_data["id"],
                    title=poetry_data["title"],
                    content=poetry_data["content"],
                    author_id=poetry_data.get("author_id"),
                    dynasty=poetry_data["dynasty"],
                    type=poetry_data.get("type"),
                    tags=poetry_data.get("tags"),
                    translation=poetry_data.get("translation"),
                    annotation=poetry_data.get("annotation"),
                    appreciation=poetry_data.get("appreciation"),
                    background=poetry_data.get("background"),
                    read_count=0,
                    like_count=0,
                    comment_count=0,
                    collect_count=0,
                    status=1,  # 已发布
                )

                session.add(poetry)
                poetries_imported += 1
                print(f"   ✅ 导入诗词: {poetry_data['title']} - {poetry_data['dynasty']} {poetry_data.get('type', '')}")

            await session.commit()
            print(f"\n✅ 诗词数据导入完成，成功导入 {poetries_imported} 首诗词")

            # 统计导入结果
            print("\n" + "="*50)
            print("📊 数据导入统计")
            print("="*50)

            # 统计作者总数
            result = await session.execute(select(Author))
            total_authors = len(result.scalars().all())
            print(f"   作者总数: {total_authors}")

            # 统计诗词总数
            result = await session.execute(select(Poetry))
            total_poetries = len(result.scalars().all())
            print(f"   诗词总数: {total_poetries}")

            # 按朝代统计
            print("\n   按朝代统计:")
            for dynasty in ["唐", "宋"]:
                result = await session.execute(
                    select(Poetry).where(Poetry.dynasty == dynasty)
                )
                count = len(result.scalars().all())
                print(f"     {dynasty}代: {count} 首")

            print("\n✅ 数据导入完成！")

        except Exception as e:
            print(f"\n❌ 导入失败: {str(e)}")
            await session.rollback()
            raise
        finally:
            await engine.dispose()


def main():
    """主函数"""
    print("="*50)
    print("🚀 星语诗词平台 - 数据导入工具")
    print("="*50)
    print()

    try:
        asyncio.run(import_data())
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断导入")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 导入过程出错: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
