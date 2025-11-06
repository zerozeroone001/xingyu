#!/bin/bash

# ==================================
# 星语诗词平台 - 停止服务脚本
# ==================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# 检查 Docker Compose 命令
if docker compose version &> /dev/null; then
    DOCKER_COMPOSE_CMD="docker compose"
else
    DOCKER_COMPOSE_CMD="docker-compose"
fi

echo ""
echo "======================================"
echo "   星语诗词平台 - 停止服务"
echo "======================================"
echo ""

# 询问是否删除数据卷
read -p "是否删除数据卷（会清空所有数据）？(y/n，默认 n): " remove_volumes
echo ""

if [[ "$remove_volumes" == "y" || "$remove_volumes" == "Y" ]]; then
    print_warning "正在停止服务并删除数据卷..."
    $DOCKER_COMPOSE_CMD down -v
    print_success "服务已停止，数据卷已删除"
else
    print_info "正在停止服务（保留数据卷）..."
    $DOCKER_COMPOSE_CMD down
    print_success "服务已停止，数据已保留"
fi

echo ""
print_info "运行 './start.sh' 重新启动服务"
echo ""
