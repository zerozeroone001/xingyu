# 切换到纯 Vue 3 版本的脚本

Write-Host "正在切换到纯 Vue 3 版本..." -ForegroundColor Green

# 备份原文件
Write-Host "备份原文件..." -ForegroundColor Yellow
Copy-Item vite.config.ts vite.config.uni.ts.bak -Force -ErrorAction SilentlyContinue
Copy-Item tsconfig.json tsconfig.uni.json.bak -Force -ErrorAction SilentlyContinue
Copy-Item src/App.vue src/App.uni.vue.bak -Force -ErrorAction SilentlyContinue
Copy-Item src/main.ts src/main.uni.ts.bak -Force -ErrorAction SilentlyContinue

# 使用简化配置
Write-Host "应用简化配置..." -ForegroundColor Yellow
Copy-Item vite.config.simple.ts vite.config.ts -Force
Copy-Item tsconfig.simple.json tsconfig.json -Force
Copy-Item src/App.simple.vue src/App.vue -Force
Copy-Item src/main.simple.ts src/main.ts -Force

Write-Host "切换完成！现在可以运行 'npm run dev' 启动开发服务器。" -ForegroundColor Green
Write-Host "访问地址: http://localhost:5173/" -ForegroundColor Cyan
