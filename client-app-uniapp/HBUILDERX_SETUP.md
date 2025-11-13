# HBuilderX 编译问题解决方案

## 问题：找不到 'pinia' 模块

```
文件查找失败：'pinia' at main.js:16
```

这个问题是因为 HBuilderX 使用的构建系统与标准的 Vue CLI 有所不同。

---

## 🔧 解决方案

### 方案 1：使用 HBuilderX 内置终端安装依赖（推荐）

1. **在 HBuilderX 中打开项目**
2. **点击菜单：工具 → 外部命令 → npm install**
3. **或者在 HBuilderX 底部的终端中执行**：
   ```bash
   npm install --legacy-peer-deps
   ```
4. **重启 HBuilderX**
5. **重新运行项目**

### 方案 2：手动安装 Pinia

1. **在项目目录打开终端**（使用 HBuilderX 的内置终端）
2. **执行命令**：
   ```bash
   npm install pinia@2.1.6 --save
   ```
3. **重新编译项目**

### 方案 3：清理缓存

1. **在 HBuilderX 菜单栏：运行 → 停止**
2. **运行 → 清理编译缓存**
3. **删除 `unpackage` 目录**
4. **重新运行项目**

### 方案 4：检查 node_modules

1. **确保 `node_modules` 目录存在**
2. **检查 `node_modules/pinia` 是否存在**
3. **如果不存在，在项目根目录执行**：
   ```bash
   rm -rf node_modules package-lock.json
   npm install --legacy-peer-deps
   ```

### 方案 5：临时禁用 Pinia（快速测试）

如果你只是想快速看到项目运行效果，可以暂时禁用 Pinia：

**修改 `main.js`：**

```javascript
import { createSSRApp } from 'vue'
// import { createPinia } from 'pinia'  // 暂时注释
import App from './App.vue'

export function createApp() {
  const app = createSSRApp(App)

  // 暂时注释 Pinia
  // const pinia = createPinia()
  // app.use(pinia)

  return {
    app
  }
}
```

**注意**：这样做后，主题切换、用户登录等功能会失效，但首页可以显示。

---

## 🎯 推荐做法

### 如果你使用的是 HBuilderX：

1. **确保使用 HBuilderX 3.6+ 版本**
2. **在 HBuilderX 中打开终端**（不要使用外部终端）
3. **执行**：
   ```bash
   npm install --legacy-peer-deps
   ```
4. **重启 HBuilderX**

### 如果你使用的是命令行（推荐）：

使用标准的 Vue CLI 命令：

```bash
# 安装依赖
npm install --legacy-peer-deps

# 运行 H5
npm run dev:h5

# 运行小程序
npm run dev:mp-weixin
```

---

## 📝 验证安装

执行以下命令验证 Pinia 是否正确安装：

```bash
# 检查 package.json
cat package.json | grep pinia

# 检查 node_modules
ls node_modules | grep pinia

# 或者在 Node.js 中测试
node -e "console.log(require('pinia'))"
```

如果输出了 Pinia 的版本信息或模块对象，说明安装成功。

---

## 🔍 其他可能的问题

### 1. HBuilderX 版本过低

- **解决**：升级到 HBuilderX 3.6 或更高版本

### 2. npm 版本问题

- **解决**：升级 npm
  ```bash
  npm install -g npm@latest
  ```

### 3. Node.js 版本问题

- **要求**：Node.js 16.0 或更高版本
- **检查**：
  ```bash
  node -v
  ```

### 4. 依赖冲突

- **解决**：使用 `--legacy-peer-deps` 参数
  ```bash
  npm install --legacy-peer-deps
  ```

---

## ✅ 成功标志

编译成功后，你应该看到类似的输出：

```
INFO  Starting development server...
 DONE  Compiled successfully
```

并且不会再出现 "文件查找失败：'pinia'" 的错误。

---

## 🆘 如果问题仍然存在

请尝试以下步骤：

1. **完全删除项目依赖**：
   ```bash
   rm -rf node_modules package-lock.json
   ```

2. **重新安装**：
   ```bash
   npm install --legacy-peer-deps
   ```

3. **清理 HBuilderX 缓存**（在 HBuilderX 中）：
   - 工具 → 清除缓存数据
   - 重启 HBuilderX

4. **使用 VS Code + 命令行**（替代方案）：
   ```bash
   npm run dev:h5
   ```

5. **联系支持**：提供完整的错误日志

---

**最后更新**: 2025-11-13
