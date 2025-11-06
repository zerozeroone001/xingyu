# 切换到纯 Vue 3 版本的步骤

## 在 PowerShell 中执行以下命令：

```powershell
# 1. 确保在 client-app 目录下
cd F:\code\python\xingyu\client-app

# 2. 备份原配置文件
Copy-Item vite.config.ts vite.config.uni.ts.bak
Copy-Item tsconfig.json tsconfig.uni.json.bak

# 3. 使用简化配置
Copy-Item vite.config.simple.ts vite.config.ts -Force
Copy-Item tsconfig.simple.json tsconfig.json -Force

# 4. 启动开发服务器
npm run dev
```

## 访问地址

启动成功后访问：http://localhost:5173/

## 如果要切换回 uni-app

```powershell
Copy-Item vite.config.uni.ts.bak vite.config.ts -Force
Copy-Item tsconfig.uni.json.bak tsconfig.json -Force
Copy-Item package.json.backup package.json -Force
```
