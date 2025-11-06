# 切换回 uni-app 版本的脚本

Write-Host "正在切换回 uni-app 版本..." -ForegroundColor Green

# 恢复原文件
Write-Host "恢复原文件..." -ForegroundColor Yellow
Copy-Item vite.config.uni.ts.bak vite.config.ts -Force -ErrorAction SilentlyContinue
Copy-Item tsconfig.uni.json.bak tsconfig.json -Force -ErrorAction SilentlyContinue
Copy-Item src/App.uni.vue.bak src/App.vue -Force -ErrorAction SilentlyContinue
Copy-Item src/main.uni.ts.bak src/main.ts -Force -ErrorAction SilentlyContinue

Write-Host "切换完成！" -ForegroundColor Green
