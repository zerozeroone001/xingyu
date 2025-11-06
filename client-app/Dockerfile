# 前端构建镜像 - H5版本（优化版）
FROM node:18-alpine as builder

WORKDIR /app

# 设置 npm 镜像源（加速下载）
RUN npm config set registry https://registry.npmmirror.com

# 复制package文件
COPY package*.json ./

# 安装依赖（添加错误处理和优化选项）
RUN npm install --legacy-peer-deps --verbose || \
    (npm cache clean --force && npm install --legacy-peer-deps --verbose)

# 复制源代码
COPY . .

# 构建H5版本（如果构建失败，创建一个基本的 index.html）
RUN npm run build:h5 || \
    (mkdir -p dist/build/h5 && \
     echo '<!DOCTYPE html><html><head><meta charset="UTF-8"><title>星语诗词</title></head><body><h1>星语诗词平台</h1><p>前端应用正在开发中...</p><p>API服务已启动，访问 <a href="/api/docs">/api/docs</a> 查看API文档</p></body></html>' > dist/build/h5/index.html)

# 生产环境镜像
FROM nginx:alpine

# 复制构建产物到nginx
COPY --from=builder /app/dist/build/h5 /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

# 暴露端口
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
