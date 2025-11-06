# 星语诗词 - 用户端应用

基于 uni-app 的多端诗词平台用户端，支持小程序和 H5。

## 功能特性

### ✨ 已实现功能

- **🎨 主题系统**
  - 明亮模式 / 暗黑模式切换
  - 主题状态持久化（本地存储）
  - 全局主题响应式更新
  - 优雅的色彩方案设计

### 🚧 规划中功能

- 诗词浏览与搜索
- 诗词收藏与点赞
- 用户社交广场
- 飞花令游戏
- 消息通知系统
- 个人中心

## 技术栈

- **框架**: uni-app 3.0 (支持微信小程序 + H5)
- **前端**: Vue 3.3.4 + TypeScript
- **状态管理**: Pinia 2.1.6
- **构建工具**: Vite 4.4.8
- **样式**: SCSS + CSS Variables

## 项目结构

```
client-app/
├── src/
│   ├── pages/              # 页面
│   │   ├── index/          # 首页
│   │   └── setting/        # 设置页
│   ├── components/         # 组件
│   │   └── theme-toggle/   # 主题切换组件
│   ├── store/              # Pinia 状态管理
│   │   ├── modules/
│   │   │   └── theme.ts    # 主题状态
│   │   └── index.ts
│   ├── utils/              # 工具函数
│   │   ├── constants.ts    # 常量定义
│   │   └── storage.ts      # 本地存储
│   ├── styles/             # 样式
│   │   ├── variables.scss  # SCSS 变量
│   │   ├── theme.scss      # 主题样式
│   │   └── common.scss     # 通用样式
│   ├── App.vue             # 根组件
│   ├── main.ts             # 入口文件
│   ├── pages.json          # 页面配置
│   └── uni.scss            # uni-app 全局样式
├── manifest.json           # 应用配置
├── package.json            # 依赖配置
├── vite.config.ts          # Vite 配置
└── tsconfig.json           # TypeScript 配置
```

## 主题系统说明

### 使用方式

#### 1. 在组件中使用主题

```vue
<template>
  <view :class="themeStore.themeClass">
    <text class="theme-text-primary">主文本</text>
    <view class="theme-card">卡片</view>
  </view>
</template>

<script setup>
import { useThemeStore } from '@/store/modules/theme';
const themeStore = useThemeStore();
</script>
```

#### 2. 使用 CSS 变量

```scss
.my-element {
  background-color: var(--bg-primary);
  color: var(--text-primary);
  border-color: var(--border-primary);
}
```

#### 3. 切换主题

```typescript
import { useThemeStore } from '@/store/modules/theme';

const themeStore = useThemeStore();

// 切换主题
themeStore.toggleTheme();

// 设置为暗黑模式
themeStore.setTheme(ThemeType.DARK);

// 设置为明亮模式
themeStore.setTheme(ThemeType.LIGHT);
```

### 可用的主题 CSS 变量

#### 颜色变量
- `--color-primary`: 主色调
- `--color-primary-light`: 主色调（浅）
- `--color-primary-dark`: 主色调（深）

#### 背景颜色
- `--bg-primary`: 主背景色
- `--bg-secondary`: 次级背景色
- `--bg-tertiary`: 三级背景色
- `--bg-card`: 卡片背景色
- `--bg-hover`: 悬停背景色

#### 文本颜色
- `--text-primary`: 主文本色
- `--text-secondary`: 次级文本色
- `--text-tertiary`: 三级文本色
- `--text-disabled`: 禁用文本色
- `--text-inverse`: 反色文本

#### 边框颜色
- `--border-primary`: 主边框色
- `--border-secondary`: 次级边框色

#### 功能色
- `--color-success`: 成功色
- `--color-warning`: 警告色
- `--color-error`: 错误色
- `--color-info`: 信息色

#### 阴影
- `--shadow-sm`: 小阴影
- `--shadow-md`: 中阴影
- `--shadow-lg`: 大阴影

### 可用的主题工具类

```scss
// 背景色
.theme-bg-primary
.theme-bg-secondary
.theme-bg-card

// 文本色
.theme-text-primary
.theme-text-secondary
.theme-text-tertiary

// 边框
.theme-border

// 卡片
.theme-card

// 按钮
.theme-button
.theme-button.button-secondary
.theme-button.button-text
```

## 开发指南

### 安装依赖

```bash
npm install
# 或
yarn install
```

### 开发模式

```bash
# 微信小程序
npm run dev:mp-weixin

# H5
npm run dev:h5
```

### 生产构建

```bash
# 微信小程序
npm run build:mp-weixin

# H5
npm run build:h5
```

### 类型检查

```bash
npm run type-check
```

## 环境要求

- Node.js >= 16
- npm >= 8 或 yarn >= 1.22

## 配置说明

### API 配置

在 `src/utils/constants.ts` 中配置 API 地址：

```typescript
export const API_BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000/api/v1'
  : 'https://api.xingyu.com/api/v1';
```

### 小程序配置

在 `manifest.json` 中配置小程序 appid：

```json
{
  "mp-weixin": {
    "appid": "你的小程序appid"
  }
}
```

## 贡献指南

欢迎提交 Issue 和 Pull Request！

## 许可证

MIT
