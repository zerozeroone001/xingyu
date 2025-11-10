#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从 chinese-poetry 项目导入唐诗数据

数据源: https://github.com/chinese-poetry/chinese-poetry
"""

import asyncio
import json
import sys
import hashlib
import io
from pathlib import Path
from typing import List, Dict, Any

# 设置标准输出为UTF-8编码（Windows兼容）
if sys.platform == 'win32':
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# 添加项目根目录到Python路径
sys.path.append(str(Path(__file__).parent.parent))

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from opencc import OpenCC

from app.core.config import settings
from app.models.author import Author
from app.models.poetry import Poetry


# 数据源路径
POETRY_DATA_DIR = Path("F:/code/python/chinese-poetry/全唐诗")

# 创建繁体转简体转换器
cc = OpenCC('t2s')  # Traditional to Simplified


def generate_id(text: str) -> int:
    """根据文本生成唯一的整数ID"""
    # 使用MD5哈希生成，取前16位转为整数
    hash_obj = hashlib.md5(text.encode('utf-8'))
    hash_hex = hash_obj.hexdigest()[:16]
    return int(hash_hex, 16) % (10**18)  # 限制在18位数字内


def clean_text(text: str) -> str:
    """清理文本，去除多余空格"""
    return ' '.join(text.split()).strip()


def convert_to_simplified(text: str | None) -> str | None:
    """
    将繁体中文转换为简体中文

    Args:
        text: 需要转换的文本，可以为None

    Returns:
        转换后的简体文本，如果输入为None则返回None
    """
    if text is None:
        return None
    return cc.convert(text)


def parse_authors(file_path: Path) -> List[Dict[str, Any]]:
    """解析作者数据"""
    print(f"📖 读取作者数据: {file_path}")

    with open(file_path, 'r', encoding='utf-8') as f:
        authors_raw = json.load(f)

    authors = []
    for author_raw in authors_raw:
        # 转换为简体中文
        name = convert_to_simplified(clean_text(author_raw['name']))
        intro = clean_text(author_raw.get('desc', '')) if author_raw.get('desc') else None
        intro = convert_to_simplified(intro)

        author = {
            'id': generate_id(f"author_{author_raw['name']}"),
            'name': name,
            'dynasty': '唐',
            'intro': intro,
        }
        authors.append(author)

    print(f"✅ 解析作者数据完成: {len(authors)} 位")
    return authors


def parse_poetries(file_path: Path, author_map: Dict[str, int], limit: int = None) -> List[Dict[str, Any]]:
    """解析诗词数据"""
    with open(file_path, 'r', encoding='utf-8') as f:
        poetries_raw = json.load(f)

    poetries = []
    count = 0

    for poetry_raw in poetries_raw:
        if limit and count >= limit:
            break

        # 组合诗句
        paragraphs = poetry_raw.get('paragraphs', [])
        content = '\n'.join(paragraphs)

        if not content.strip():
            continue

        author_name = clean_text(poetry_raw.get('author', ''))
        author_id = author_map.get(author_name)

        # 根据内容判断诗词类型
        poem_type = None
        lines = len(paragraphs)
        if lines == 4:
            poem_type = '绝句'
        elif lines == 8:
            poem_type = '律诗'
        elif lines > 8:
            poem_type = '古诗'

        # 处理标题（最大100字符）并转换为简体
        title = clean_text(poetry_raw.get('title', '无题'))
        title = convert_to_simplified(title)
        if len(title) > 100:
            title = title[:97] + '...'

        # 转换内容为简体
        content = convert_to_simplified(content)
        author_name = convert_to_simplified(author_name)

        poetry = {
            'id': generate_id(f"poetry_{poetry_raw.get('title', '')}_{author_name}_{content[:20]}"),
            'title': title,
            'content': content,
            'author_id': author_id,
            'dynasty': '唐',
            'type': poem_type,
            'tags': None,
            'translation': None,
            'annotation': None,
            'appreciation': None,
            'background': None,
            'read_count': 0,
            'like_count': 0,
            'comment_count': 0,
            'collect_count': 0,
            'status': 1,  # 已发布
        }

        poetries.append(poetry)
        count += 1

    return poetries


async def import_data(limit_per_file: int = None, max_files: int = None):
    """导入数据"""

    # 创建数据库引擎
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=False,  # 关闭SQL日志，提高导入速度
        pool_pre_ping=True,
    )

    # 创建会话工厂
    async_session = async_sessionmaker(
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    try:
        # 1. 导入作者数据
        print("\n" + "="*60)
        print("📚 第一步：导入作者数据")
        print("="*60)

        authors_file = POETRY_DATA_DIR / "authors.tang.json"
        authors_data = parse_authors(authors_file)

        # 创建作者名到ID的映射
        author_map = {author['name']: author['id'] for author in authors_data}

        async with async_session() as session:
            authors_imported = 0
            authors_skipped = 0

            for author_data in authors_data:
                # 检查是否已存在
                result = await session.execute(
                    select(Author).where(Author.id == author_data['id'])
                )
                if result.scalar_one_or_none():
                    authors_skipped += 1
                    continue

                author = Author(**author_data)
                session.add(author)
                authors_imported += 1

                if authors_imported % 100 == 0:
                    print(f"   已导入 {authors_imported} 位作者...")

            await session.commit()
            print(f"✅ 作者导入完成: 新增 {authors_imported} 位, 跳过 {authors_skipped} 位")

        # 2. 导入诗词数据
        print("\n" + "="*60)
        print("📚 第二步：导入诗词数据")
        print("="*60)

        # 获取所有诗词文件
        poetry_files = sorted(POETRY_DATA_DIR.glob("poet.tang.*.json"))

        if max_files:
            poetry_files = poetry_files[:max_files]

        print(f"📂 找到 {len(poetry_files)} 个诗词文件")

        total_poetries_imported = 0
        total_poetries_skipped = 0

        for idx, poetry_file in enumerate(poetry_files, 1):
            print(f"\n[{idx}/{len(poetry_files)}] 处理文件: {poetry_file.name}")

            poetries_data = parse_poetries(poetry_file, author_map, limit_per_file)
            print(f"   解析到 {len(poetries_data)} 首诗")

            async with async_session() as session:
                batch_imported = 0
                batch_skipped = 0

                for poetry_data in poetries_data:
                    # 检查是否已存在
                    result = await session.execute(
                        select(Poetry).where(Poetry.id == poetry_data['id'])
                    )
                    if result.scalar_one_or_none():
                        batch_skipped += 1
                        continue

                    poetry = Poetry(**poetry_data)
                    session.add(poetry)
                    batch_imported += 1

                    if batch_imported % 100 == 0:
                        await session.commit()
                        print(f"   已导入 {batch_imported} 首...")

                await session.commit()
                total_poetries_imported += batch_imported
                total_poetries_skipped += batch_skipped

                print(f"   ✅ 本文件: 新增 {batch_imported} 首, 跳过 {batch_skipped} 首")

        print(f"\n✅ 诗词导入完成: 总新增 {total_poetries_imported} 首, 跳过 {total_poetries_skipped} 首")

        # 3. 统计信息
        print("\n" + "="*60)
        print("📊 数据库统计")
        print("="*60)

        async with async_session() as session:
            # 统计作者
            result = await session.execute(select(Author))
            total_authors = len(result.scalars().all())
            print(f"   作者总数: {total_authors}")

            # 统计诗词
            result = await session.execute(select(Poetry))
            total_poetries = len(result.scalars().all())
            print(f"   诗词总数: {total_poetries}")

            # 按类型统计
            for poem_type in ['绝句', '律诗', '古诗']:
                result = await session.execute(
                    select(Poetry).where(Poetry.type == poem_type)
                )
                count = len(result.scalars().all())
                print(f"   {poem_type}: {count} 首")

        print("\n✅ 导入完成！")

    except Exception as e:
        print(f"\n❌ 导入失败: {str(e)}")
        import traceback
        traceback.print_exc()
        raise
    finally:
        await engine.dispose()


def main():
    """主函数"""
    print("="*60)
    print("🚀 星语诗词平台 - 唐诗数据导入工具")
    print("="*60)
    print(f"📂 数据源: {POETRY_DATA_DIR}")
    print()

    # 检查数据目录
    if not POETRY_DATA_DIR.exists():
        print(f"❌ 错误: 数据目录不存在: {POETRY_DATA_DIR}")
        print("\n请先克隆 chinese-poetry 项目:")
        print("   cd F:/code/python")
        print("   git clone https://github.com/chinese-poetry/chinese-poetry.git")
        sys.exit(1)

    # 配置导入参数
    import argparse
    parser = argparse.ArgumentParser(description='导入唐诗数据')
    parser.add_argument('--limit', type=int, help='每个文件最多导入的诗词数量（用于测试）')
    parser.add_argument('--max-files', type=int, help='最多处理的文件数量（用于测试）')
    args = parser.parse_args()

    if args.limit:
        print(f"⚠️  测试模式: 每个文件最多导入 {args.limit} 首诗")
    if args.max_files:
        print(f"⚠️  测试模式: 最多处理 {args.max_files} 个文件")

    print()

    try:
        asyncio.run(import_data(
            limit_per_file=args.limit,
            max_files=args.max_files
        ))
    except KeyboardInterrupt:
        print("\n\n⚠️  用户中断导入")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ 导入过程出错: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()
