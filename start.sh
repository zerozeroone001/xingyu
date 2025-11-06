#!/bin/bash

# ==================================
# 星语诗词平台 - 一键启动脚本
# ==================================

set -e

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 打印带颜色的信息
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 打印欢迎信息
print_header() {
    echo ""
    echo "======================================"
    echo "   星语诗词平台 - 一键启动部署"
    echo "======================================"
    echo ""
}

# 检查 Docker 是否安装
check_docker() {
    print_info "检查 Docker 环境..."
    if ! command -v docker &> /dev/null; then
        print_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    print_success "Docker 已安装: $(docker --version)"
}

# 检查 Docker Compose 是否安装
check_docker_compose() {
    print_info "检查 Docker Compose 环境..."
    if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null; then
        print_error "Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi

    # 优先使用 docker compose (v2)
    if docker compose version &> /dev/null; then
        DOCKER_COMPOSE_CMD="docker compose"
        print_success "Docker Compose 已安装: $(docker compose version)"
    else
        DOCKER_COMPOSE_CMD="docker-compose"
        print_success "Docker Compose 已安装: $(docker-compose --version)"
    fi
}

# 检查环境变量文件
check_env_file() {
    print_info "检查环境变量配置..."
    if [ ! -f .env ]; then
        print_warning ".env 文件不存在，将从 .env.example 创建"
        if [ -f .env.example ]; then
            cp .env.example .env
            print_success "已创建 .env 文件，使用默认配置"
            print_warning "生产环境请修改 .env 中的密钥配置！"
        else
            print_error ".env.example 文件不存在"
            exit 1
        fi
    else
        print_success ".env 文件已存在"
    fi
}

# 停止并清理旧容器
cleanup() {
    print_info "停止并清理旧容器..."
    $DOCKER_COMPOSE_CMD down
    print_success "旧容器已清理"
}

# 构建镜像
build_images() {
    print_info "构建 Docker 镜像..."
    print_info "这可能需要几分钟时间，请耐心等待..."
    $DOCKER_COMPOSE_CMD build --no-cache
    print_success "镜像构建完成"
}

# 启动服务
start_services() {
    print_info "启动所有服务..."
    $DOCKER_COMPOSE_CMD up -d
    print_success "服务已启动"
}

# 等待服务就绪
wait_for_services() {
    print_info "等待服务启动并通过健康检查..."
    print_info "这可能需要 1-2 分钟..."

    local max_attempts=60
    local attempt=0

    while [ $attempt -lt $max_attempts ]; do
        # 检查所有服务的健康状态
        local healthy_count=$($DOCKER_COMPOSE_CMD ps | grep -c "healthy" || true)
        local total_services=4  # mysql, redis, elasticsearch, api

        if [ $healthy_count -eq $total_services ]; then
            print_success "所有服务已就绪"
            return 0
        fi

        echo -n "."
        sleep 2
        attempt=$((attempt + 1))
    done

    print_warning "服务启动超时，但可能仍在初始化中"
    print_info "请运行 'docker-compose logs' 查看详细日志"
}

# 显示服务状态
show_status() {
    echo ""
    print_info "服务状态："
    $DOCKER_COMPOSE_CMD ps
    echo ""
}

# 显示访问信息
show_access_info() {
    echo ""
    print_success "======================================"
    print_success "  部署完成！服务访问地址："
    print_success "======================================"
    echo ""
    echo "  📱 前端 H5:        http://localhost:8080"
    echo "  🚀 后端 API:       http://localhost:8000"
    echo "  📚 API 文档:       http://localhost:8000/docs"
    echo "  🗄️  MySQL:          localhost:3306"
    echo "  💾 Redis:          localhost:6380"
    echo "  🔍 Elasticsearch:  http://localhost:9200"
    echo ""
    print_info "======================================"
    print_info "  常用命令："
    print_info "======================================"
    echo ""
    echo "  查看日志:    $DOCKER_COMPOSE_CMD logs -f"
    echo "  查看状态:    $DOCKER_COMPOSE_CMD ps"
    echo "  停止服务:    $DOCKER_COMPOSE_CMD down"
    echo "  重启服务:    $DOCKER_COMPOSE_CMD restart"
    echo "  进入容器:    docker exec -it poetry-api bash"
    echo ""
}

# 主函数
main() {
    print_header

    # 检查环境
    check_docker
    check_docker_compose
    check_env_file

    # 询问是否清理旧容器
    read -p "是否清理旧容器？(y/n，默认 n): " cleanup_choice
    if [[ "$cleanup_choice" == "y" || "$cleanup_choice" == "Y" ]]; then
        cleanup
    fi

    # 询问是否重新构建镜像
    read -p "是否重新构建镜像？(y/n，默认 n): " build_choice
    if [[ "$build_choice" == "y" || "$build_choice" == "Y" ]]; then
        build_images
    fi

    # 启动服务
    start_services

    # 等待服务就绪
    wait_for_services

    # 显示状态
    show_status

    # 显示访问信息
    show_access_info
}

# 运行主函数
main
