# 前端 Docker 构建说明

## 问题说明

如果在构建前端时遇到 `npm install` 失败的错误，这通常是因为：
1. uni-app 的 alpha 版本依赖可能不稳定
2. 缺少 package-lock.json 文件
3. npm 依赖版本冲突

## 解决方案

我们提供了两种构建方案：

### 方案一：完整构建（默认）

使用 `Dockerfile`，会尝试构建完整的 uni-app H5 应用。

**特点**：
- 使用国内 npm 镜像源加速下载
- 添加 `--legacy-peer-deps` 选项处理依赖冲突
- 如果构建失败，自动回退到简单的 HTML 页面

**构建命令**：
```bash
docker compose build web
```

### 方案二：简化版（推荐用于快速测试）

使用 `Dockerfile.simple`，直接部署静态 HTML 页面。

**特点**：
- 构建速度快（几秒钟）
- 无需 npm 依赖
- 包含完整的主题切换功能
- 展示项目信息和链接到 API 文档

**使用方法**：

#### 修改 docker-compose.yml

找到 web 服务配置，修改 dockerfile 路径：

```yaml
# 前端应用 (H5)
web:
  build:
    context: ./client-app
    dockerfile: Dockerfile.simple  # 改为使用简化版
  container_name: poetry-web
  # ... 其他配置保持不变
```

#### 或者直接构建

```bash
cd client-app
docker build -f Dockerfile.simple -t poetry-web-simple .
```

## 功能对比

| 功能 | Dockerfile（完整版） | Dockerfile.simple（简化版） |
|------|---------------------|---------------------------|
| 构建时间 | 5-10 分钟 | 几秒钟 |
| 文件大小 | ~500MB | ~20MB |
| 主题切换 | ✅ | ✅ |
| 响应式设计 | ✅ | ✅ |
| 完整 uni-app 功能 | ✅ | ❌ |
| 静态展示页面 | ❌ | ✅ |

## 推荐使用场景

### 使用完整版 Dockerfile
- 需要完整的 uni-app 功能
- 准备正式部署
- 有充足的构建时间

### 使用简化版 Dockerfile.simple
- 快速测试部署流程
- npm install 持续失败
- 主要测试后端 API
- 演示用途

## 完整构建故障排查

如果完整构建失败，请检查：

1. **网络连接**
```bash
# 测试 npm 镜像源
curl https://registry.npmmirror.com
```

2. **Docker 资源限制**
```bash
# 查看 Docker 资源使用
docker stats
```

3. **查看详细构建日志**
```bash
docker compose build --no-cache --progress=plain web
```

4. **手动测试 npm install**
```bash
cd client-app
npm config set registry https://registry.npmmirror.com
npm install --legacy-peer-deps
```

## 当前静态页面功能

简化版包含以下功能：
- ✅ 响应式布局
- ✅ 明亮/暗黑主题切换
- ✅ 主题持久化（LocalStorage）
- ✅ 项目介绍和功能展示
- ✅ 链接到 API 文档
- ✅ 服务状态展示
- ✅ 优雅的 UI 设计

## 下一步开发

待 uni-app 环境稳定后，可以：
1. 生成 package-lock.json
2. 使用稳定版本的 uni-app 依赖
3. 添加本地依赖缓存
4. 使用多阶段构建优化

## 快速切换方法

在 docker-compose.yml 中保留两个配置的注释：

```yaml
web:
  build:
    context: ./client-app
    # 完整版（默认）
    dockerfile: Dockerfile
    # 简化版（快速）
    # dockerfile: Dockerfile.simple
```

需要切换时，只需注释/取消注释相应行，然后重新构建：

```bash
docker compose up -d --build web
```
