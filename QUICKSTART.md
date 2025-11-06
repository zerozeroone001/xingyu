# 快速开始指南

## 一键启动

只需3步，即可启动整个星语诗词平台：

### 1. 确保已安装 Docker

```bash
# 检查 Docker 是否已安装
docker --version
docker-compose --version
```

如果未安装，请参考 [DEPLOYMENT.md](./DEPLOYMENT.md) 的安装说明。

### 2. 运行启动脚本

```bash
./start.sh
```

脚本会自动：
- ✅ 检查 Docker 环境
- ✅ 创建配置文件（如果不存在）
- ✅ 构建 Docker 镜像
- ✅ 启动所有服务（MySQL、Redis、Elasticsearch、后端API、前端H5）
- ✅ 等待服务就绪
- ✅ 显示访问地址

### 3. 访问应用

启动完成后，在浏览器打开：

- 📱 **前端应用**: http://localhost:8080
- 🚀 **后端API**: http://localhost:8000
- 📚 **API文档**: http://localhost:8000/docs

## 服务说明

启动后，将运行以下服务：

| 服务 | 地址 | 说明 |
|------|------|------|
| 前端H5 | http://localhost:8080 | Vue3/uni-app 前端应用 |
| 后端API | http://localhost:8000 | FastAPI 后端服务 |
| API文档 | http://localhost:8000/docs | Swagger 交互式文档 |
| MySQL | localhost:3306 | 数据库 |
| Redis | localhost:6380 | 缓存服务 |
| Elasticsearch | http://localhost:9200 | 搜索引擎 |

## 常用命令

```bash
# 查看服务状态
docker-compose ps

# 查看日志
docker-compose logs -f

# 查看特定服务日志
docker-compose logs -f api
docker-compose logs -f web

# 重启服务
docker-compose restart

# 停止服务（保留数据）
./stop.sh

# 停止服务并删除数据
./stop.sh  # 选择 y 删除数据卷
```

## 初始化数据（可选）

如需导入诗词数据：

```bash
# 进入后端容器
docker exec -it poetry-api bash

# 运行数据库迁移
alembic upgrade head

# 导入诗词数据
python scripts/import_poetry.py

# 退出容器
exit
```

## 开发模式

服务启动后支持热重载：

- **后端**: 修改 `server/` 目录下的 Python 代码会自动重载
- **前端**: 需要在开发环境运行 `npm run dev:h5`

## 故障排查

### 端口被占用

如果端口被占用，可以修改 `docker-compose.yml` 中的端口映射。

### 服务启动失败

```bash
# 查看详细日志
docker-compose logs

# 重新构建并启动
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### 数据库连接失败

等待 30-60 秒让 MySQL 完全启动，然后重启 API 服务：

```bash
docker-compose restart api
```

## 更多信息

详细的部署说明和运维管理，请查看：

- [完整部署文档](./DEPLOYMENT.md)
- [项目说明](./README.md)
- [开发计划](./最终开发计划.md)

---

**祝使用愉快！** 🎉
