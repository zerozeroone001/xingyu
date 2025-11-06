#!/bin/bash
# 一键切换到 Web 版本的脚本

echo "正在切换到纯 Web 版本..."

# 1. 备份原文件
echo "备份原文件..."
cp package.json package.json.uni.bak 2>/dev/null || true
cp vite.config.ts vite.config.uni.bak 2>/dev/null || true
cp tsconfig.json tsconfig.uni.bak 2>/dev/null || true
cp src/App.vue src/App.uni.bak 2>/dev/null || true
cp src/main.ts src/main.uni.bak 2>/dev/null || true

# 2. 应用简化配置
echo "应用 Web 版本配置..."
cp package.simple.json package.json
cp vite.config.simple.ts vite.config.ts
cp tsconfig.simple.json tsconfig.json
cp src/App.simple.vue src/App.vue
cp src/main.simple.ts src/main.ts

echo "✅ 文件切换完成！"
echo ""
echo "现在请执行以下命令："
echo "1. npm install"
echo "2. npm install vue-router@4"
echo "3. npm run dev"
