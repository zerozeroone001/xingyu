#!/bin/bash

# 星语诗词平台 - API 入口脚本
# 处理 Windows CRLF 问题并启动服务

set -e

echo "正在等待数据库就绪..."
sleep 5

echo "运行数据库迁移..."
alembic upgrade head

echo "启动 API 服务..."
exec uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
