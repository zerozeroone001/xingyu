#!/bin/bash

# 星语诗词平台 - API 简化入口脚本（跳过数据库迁移）

set -e

echo "正在等待数据库就绪..."
sleep 10

echo "跳过数据库迁移..."
echo "如需运行迁移，请执行: docker exec poetry-api alembic upgrade head"

echo "启动 API 服务..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload