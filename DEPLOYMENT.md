# 星语诗词平台 - Docker 部署指南

## 📋 目录

- [系统要求](#系统要求)
- [快速开始](#快速开始)
- [详细部署步骤](#详细部署步骤)
- [服务配置](#服务配置)
- [常见问题](#常见问题)
- [运维管理](#运维管理)

## 🔧 系统要求

### 必需软件

- **Docker**: >= 20.10
- **Docker Compose**: >= 2.0 (或 docker-compose >= 1.29)
- **操作系统**: Linux / macOS / Windows (with WSL2)

### 硬件要求

**最低配置**:
- CPU: 2核
- 内存: 4GB
- 磁盘: 20GB

**推荐配置**:
- CPU: 4核+
- 内存: 8GB+
- 磁盘: 50GB+

## 🚀 快速开始

### 一键启动

```bash
# 1. 克隆项目（如果还没有）
git clone <your-repo-url>
cd xingyu

# 2. 运行一键启动脚本
chmod +x start.sh
./start.sh
```

脚本会自动完成：
- ✅ 检查 Docker 环境
- ✅ 创建 .env 配置文件
- ✅ 构建 Docker 镜像
- ✅ 启动所有服务
- ✅ 等待服务健康检查
- ✅ 显示访问地址

### 访问服务

启动成功后，可以通过以下地址访问：

- 📱 **前端 H5**: http://localhost:8080
- 🚀 **后端 API**: http://localhost:8000
- 📚 **API 文档**: http://localhost:8000/docs
- 🗄️ **MySQL**: localhost:3306
- 💾 **Redis**: localhost:6380
- 🔍 **Elasticsearch**: http://localhost:9200

### 停止服务

```bash
# 运行停止脚本
chmod +x stop.sh
./stop.sh
```

## 📝 详细部署步骤

### 第一步：环境准备

#### 1. 安装 Docker

**Linux (Ubuntu/Debian)**:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**macOS**:
```bash
brew install --cask docker
```

**Windows**:
下载并安装 [Docker Desktop](https://www.docker.com/products/docker-desktop)

#### 2. 验证安装

```bash
docker --version
docker-compose --version
# 或
docker compose version
```

### 第二步：配置环境变量

```bash
# 复制示例配置文件
cp .env.example .env

# 编辑配置文件（生产环境必须修改密钥！）
vim .env
```

**重要配置项**:

```bash
# 数据库配置
MYSQL_ROOT_PASSWORD=your_secure_password_here
MYSQL_DATABASE=poetry_db

# 安全密钥（生产环境务必修改！）
SECRET_KEY=your_secret_key_here
JWT_SECRET_KEY=your_jwt_secret_key_here

# CORS 配置
CORS_ORIGINS=http://your-domain.com,https://your-domain.com
```

### 第三步：构建和启动

#### 方式一：使用一键脚本（推荐）

```bash
chmod +x start.sh
./start.sh
```

#### 方式二：手动执行

```bash
# 1. 构建镜像
docker compose build

# 2. 启动服务
docker compose up -d

# 3. 查看日志
docker compose logs -f
```

### 第四步：初始化数据库

```bash
# 进入后端容器
docker exec -it poetry-api bash

# 运行数据库迁移
alembic upgrade head

# 导入诗词数据（可选）
python scripts/import_poetry.py

# 退出容器
exit
```

## ⚙️ 服务配置

### 服务列表

| 服务名 | 容器名 | 端口 | 说明 |
|--------|--------|------|------|
| mysql | poetry-mysql | 3306 | MySQL 8.0 数据库 |
| redis | poetry-redis | 6380 | Redis 7 缓存 |
| elasticsearch | poetry-es | 9200 | Elasticsearch 7.17 搜索引擎 |
| api | poetry-api | 8000 | FastAPI 后端服务 |
| web | poetry-web | 8080 | Vue3/uni-app 前端 H5 |

### 网络配置

所有服务运行在 `poetry-network` 网络中，服务间可通过容器名直接通信。

### 数据持久化

以下数据卷用于持久化存储：

- `mysql_data`: MySQL 数据
- `redis_data`: Redis 数据
- `es_data`: Elasticsearch 索引数据

## 🔍 常见问题

### Q1: 端口被占用

**错误**: `Bind for 0.0.0.0:8080 failed: port is already allocated`

**解决方案**:
```bash
# 修改 docker-compose.yml 中的端口映射
# 将 "8080:80" 改为 "8081:80"
```

### Q2: 内存不足

**错误**: Elasticsearch 启动失败

**解决方案**:
```bash
# 调整 Elasticsearch 内存限制
# 在 docker-compose.yml 中修改:
environment:
  - "ES_JAVA_OPTS=-Xms256m -Xmx256m"  # 降低内存使用
```

### Q3: MySQL 连接失败

**错误**: `Can't connect to MySQL server`

**解决方案**:
```bash
# 等待 MySQL 完全启动（需要 30-60 秒）
docker compose logs mysql

# 检查健康状态
docker compose ps
```

### Q4: 前端无法访问后端

**解决方案**:
```bash
# 1. 检查 CORS 配置
# 在 .env 中添加前端地址:
CORS_ORIGINS=http://localhost:8080

# 2. 重启服务
docker compose restart api
```

### Q5: 数据库迁移失败

**解决方案**:
```bash
# 1. 进入后端容器
docker exec -it poetry-api bash

# 2. 检查数据库连接
python -c "from app.core.database import engine; print(engine)"

# 3. 重新运行迁移
alembic upgrade head
```

## 🛠️ 运维管理

### 查看服务状态

```bash
# 查看所有服务状态
docker compose ps

# 查看特定服务状态
docker compose ps api
```

### 查看日志

```bash
# 查看所有服务日志
docker compose logs

# 实时查看日志
docker compose logs -f

# 查看特定服务日志
docker compose logs api
docker compose logs web

# 查看最近 100 行日志
docker compose logs --tail=100
```

### 重启服务

```bash
# 重启所有服务
docker compose restart

# 重启特定服务
docker compose restart api
docker compose restart web
```

### 进入容器

```bash
# 进入后端容器
docker exec -it poetry-api bash

# 进入前端容器
docker exec -it poetry-web sh

# 进入数据库容器
docker exec -it poetry-mysql bash
```

### 备份数据

#### 备份 MySQL

```bash
# 备份数据库
docker exec poetry-mysql mysqldump -u root -ppoetry_root_2024 poetry_db > backup_$(date +%Y%m%d).sql

# 恢复数据库
docker exec -i poetry-mysql mysql -u root -ppoetry_root_2024 poetry_db < backup_20240101.sql
```

#### 备份 Redis

```bash
# 备份 Redis 数据
docker exec poetry-redis redis-cli SAVE
docker cp poetry-redis:/data/dump.rdb ./redis_backup_$(date +%Y%m%d).rdb
```

### 清理资源

```bash
# 停止并删除容器（保留数据卷）
docker compose down

# 停止并删除容器和数据卷
docker compose down -v

# 清理未使用的镜像
docker image prune -a

# 清理所有未使用资源
docker system prune -a
```

### 更新服务

```bash
# 1. 拉取最新代码
git pull

# 2. 重新构建镜像
docker compose build --no-cache

# 3. 重启服务
docker compose up -d
```

### 扩容服务

```bash
# 扩展后端服务到 3 个实例
docker compose up -d --scale api=3
```

### 性能监控

```bash
# 查看资源使用情况
docker stats

# 查看特定容器资源使用
docker stats poetry-api poetry-web
```

## 🔒 生产环境建议

### 安全配置

1. **修改默认密钥**:
   ```bash
   # 使用强密码和密钥
   openssl rand -hex 32  # 生成随机密钥
   ```

2. **限制端口暴露**:
   ```yaml
   # 仅在内网暴露
   ports:
     - "127.0.0.1:3306:3306"
   ```

3. **使用 HTTPS**:
   ```bash
   # 配置 Nginx 反向代理 + SSL
   # 使用 Let's Encrypt 证书
   ```

### 性能优化

1. **调整资源限制**:
   ```yaml
   services:
     api:
       deploy:
         resources:
           limits:
             cpus: '2'
             memory: 2G
           reservations:
             cpus: '1'
             memory: 1G
   ```

2. **启用 Redis 持久化**:
   ```yaml
   redis:
     command: redis-server --appendonly yes
   ```

3. **配置日志轮转**:
   ```yaml
   logging:
     driver: "json-file"
     options:
       max-size: "10m"
       max-file: "3"
   ```

### 高可用部署

1. **使用 Docker Swarm 或 Kubernetes**
2. **配置负载均衡**
3. **设置数据库主从复制**
4. **使用 Redis Sentinel**

## 📞 技术支持

如遇到问题，请：

1. 查看日志: `docker compose logs`
2. 检查服务状态: `docker compose ps`
3. 查阅本文档的常见问题部分
4. 提交 Issue 到项目仓库

## 📚 相关文档

- [项目 README](./README.md)
- [开发计划](./最终开发计划.md)
- [后端运行指南](./server/运行指南.md)
- [前端 README](./client-app/README.md)

---

**祝部署顺利！** 🎉
