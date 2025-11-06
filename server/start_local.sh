#!/bin/bash

# 星语诗词平台 - 本地开发启动脚本

echo "=========================================="
echo "  星语诗词平台 - 本地开发环境启动"
echo "=========================================="
echo ""

# 检查 Python 虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建 Python 虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
if [ ! -f "venv/.deps_installed" ]; then
    echo "📥 安装 Python 依赖..."
    pip install -r requirements.txt
    touch venv/.deps_installed
fi

# 检查 .env 文件
if [ ! -f ".env" ]; then
    echo "⚠️  .env 文件不存在，从 .env.example 复制..."
    cp .env.example .env
    echo "⚠️  请编辑 .env 文件配置数据库等信息"
    exit 1
fi

echo ""
echo "✅ 环境准备完成"
echo ""
echo "📝 注意事项："
echo "   1. 请确保 MySQL 数据库已启动（端口 3306）"
echo "   2. 请确保 Redis 已启动（端口 6379）"
echo "   3. 首次运行需要执行数据库迁移："
echo "      alembic upgrade head"
echo ""
echo "🚀 启动应用..."
echo ""

# 启动应用
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
