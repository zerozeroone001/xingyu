# 一键切换到 Web 版本的脚本
Write-Host "正在切换到纯 Web 版本..." -ForegroundColor Green

# 1. 停止提示确认
$ErrorActionPreference = 'SilentlyContinue'

# 2. 备份原文件
Write-Host "备份原文件..." -ForegroundColor Yellow
Copy-Item package.json package.json.uni.bak -Force
Copy-Item vite.config.ts vite.config.uni.bak -Force
Copy-Item tsconfig.json tsconfig.uni.bak -Force
Copy-Item src/App.vue src/App.uni.bak -Force
Copy-Item src/main.ts src/main.uni.bak -Force

# 3. 应用简化配置
Write-Host "应用 Web 版本配置..." -ForegroundColor Yellow
Copy-Item package.simple.json package.json -Force
Copy-Item vite.config.simple.ts vite.config.ts -Force
Copy-Item tsconfig.simple.json tsconfig.json -Force
Copy-Item src/App.simple.vue src/App.vue -Force
Copy-Item src/main.simple.ts src/main.ts -Force

Write-Host ""
Write-Host "✅ 文件切换完成！" -ForegroundColor Green
Write-Host ""
Write-Host "现在请执行以下命令：" -ForegroundColor Cyan
Write-Host "1. Remove-Item -Recurse -Force node_modules" -ForegroundColor White
Write-Host "2. npm install" -ForegroundColor White
Write-Host "3. npm install vue-router@4" -ForegroundColor White
Write-Host "4. npm run dev" -ForegroundColor White
