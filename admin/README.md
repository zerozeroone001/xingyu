# 星语诗词管理后台

技术栈：Vue 2 + Element UI + Axios。后台接口使用现有 FastAPI 服务的 `/api/v1/admin/*`。

## 启动

先启动后端：

```powershell
cd F:\code\python\xingyu\backend
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000
```

如果 `8000` 上已经有旧后端进程，管理登录会返回 404。请先停止旧进程后重启，或临时换端口：

```powershell
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001
```

换端口时，在登录页把接口地址改为：

```text
http://127.0.0.1:8001/api/v1
```

再启动管理端静态服务：

```powershell
cd F:\code\python\xingyu\admin
npm run dev
```

访问：

```text
http://127.0.0.1:5173
```

如果 `5173` 被占用，启动脚本会自动尝试后续端口。也可以手动指定：

```powershell
npm run dev -- --port 5174
```

默认管理员：

```text
账号：admin
密码：admin123456
```

生产部署时通过环境变量覆盖：

```powershell
$env:ADMIN_USERNAME="your-admin"
$env:ADMIN_PASSWORD="your-strong-password"
```
