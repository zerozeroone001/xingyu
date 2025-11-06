# 星语诗词平台 - 后端服务

基于 FastAPI + SQLAlchemy 2.0 + MySQL 的高性能异步后端服务。

## 技术栈

- **Python**: 3.11+
- **Web框架**: FastAPI 0.104.1
- **ORM**: SQLAlchemy 2.0.23 (异步)
- **数据库**: MySQL 8.0
- **缓存**: Redis 7.0
- **搜索**: Elasticsearch 7.17

## 项目结构

```
server/
├── app/
│   ├── api/            # API路由
│   ├── core/           # 核心配置
│   ├── models/         # 数据模型
│   ├── schemas/        # Pydantic模型
│   ├── services/       # 业务逻辑
│   └── main.py         # 应用入口
├── tests/              # 测试
├── requirements.txt    # 依赖
├── .env.example        # 环境变量示例
└── Dockerfile          # Docker镜像
```

## 快速开始

### 1. 环境要求

- Python 3.11+
- MySQL 8.0+
- Redis 7.0+

### 2. 安装依赖

```bash
# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息
```

### 4. 初始化数据库

```bash
# 运行数据库迁移
alembic upgrade head
```

### 5. 启动服务

```bash
# 开发模式
uvicorn app.main:app --reload

# 或使用
python app/main.py
```

访问 http://localhost:8000/docs 查看API文档。

## 使用Docker

### 启动所有服务

```bash
# 在项目根目录执行
docker-compose up -d
```

这将启动：
- MySQL (端口 3306)
- Redis (端口 6379)
- Elasticsearch (端口 9200)
- FastAPI应用 (端口 8000)

### 查看日志

```bash
docker-compose logs -f api
```

### 停止服务

```bash
docker-compose down
```

## API文档

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 核心功能

### 已实现

- ✅ 用户注册/登录
- ✅ JWT认证
- ✅ 用户信息管理

### 开发中

- 🔨 诗词CRUD
- 🔨 诗词搜索
- 🔨 AI功能集成
- 🔨 飞花令游戏

## 测试

```bash
# 运行测试
pytest tests/

# 查看覆盖率
pytest --cov=app tests/
```

## 代码规范

```bash
# 格式化代码
black app/

# 代码检查
ruff check app/

# 类型检查
mypy app/
```

## 环境变量说明

| 变量名 | 说明 | 示例 |
|--------|------|------|
| DATABASE_URL | 数据库连接URL | mysql+aiomysql://user:pass@localhost/db |
| REDIS_URL | Redis连接URL | redis://localhost:6379/0 |
| SECRET_KEY | 应用密钥 | your-secret-key |
| JWT_SECRET_KEY | JWT密钥 | your-jwt-secret |
| TONGYI_API_KEY | 通义千问API密钥 | sk-xxx |

## 开发计划

参见项目根目录的 `最终开发计划.md`

## 许可证

MIT License
