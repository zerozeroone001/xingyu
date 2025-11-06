#!/bin/bash

# 星语诗词平台 - API 启动脚本
# 先运行数据库迁移，然后启动 API 服务

set -e

echo "正在等待数据库就绪..."
sleep 5

echo "运行数据库迁移..."
alembic upgrade head

echo "启动 API 服务..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
