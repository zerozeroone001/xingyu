# 星语诗词 - UniApp 客户端

> 面向诗词爱好者的多端互动平台 - UniApp 重构版本

## 项目简介

这是星语诗词平台的 UniApp 客户端重构版本，采用 Vue 3 + UniApp 框架开发，支持微信小程序和 H5 多端运行。

## 核心特性

### ✨ 主题系统（重点功能）

- **10种精美主题**：明亮、暗黑、清新、炫紫、温馨、海洋、森林、晚霞、星空、简约
- **流畅过渡动画**：主题切换时的平滑过渡效果
- **完整配色方案**：每个主题包含背景色、文字色、按钮色等完整配色
- **实时生效**：主题切换立即应用到所有页面和组件

### 📱 功能完善

- ✅ 用户认证（微信登录 + 账号密码登录）
- ✅ 每日诗词推荐
- ✅ 诗词浏览和搜索
- ✅ 点赞、收藏、评论
- ✅ 个人中心和用户信息
- ✅ 消息系统
- ✅ 广场（用户内容发布）
- ✅ 飞花令游戏
- ✅ 作者列表和详情

### 🎨 界面设计

- **美观大方**：精心设计的 UI 界面
- **响应式布局**：适配各种屏幕尺寸
- **流畅动画**：丰富的交互动画效果
- **缺省状态**：完善的空状态和加载状态

### 💻 代码质量

- **优雅架构**：清晰的项目结构和代码组织
- **详细注释**：所有关键代码都有详细注释
- **TypeScript 支持**：部分代码使用 TypeScript
- **统一规范**：统一的代码风格和命名规范

## 技术栈

- **框架**：Vue 3 + UniApp 3.0
- **状态管理**：Pinia
- **样式**：SCSS + CSS Variables
- **构建工具**：Vite
- **UI 组件**：uni-ui + 自定义组件

## 项目结构

```
client-app-uniapp/
├── api/                    # API 接口封装
│   ├── auth.js            # 认证相关
│   ├── user.js            # 用户相关
│   ├── poetry.js          # 诗词相关
│   ├── author.js          # 作者相关
│   ├── square.js          # 广场相关
│   ├── comment.js         # 评论相关
│   ├── message.js         # 消息相关
│   └── game.js            # 游戏相关
│
├── components/            # 通用组件
│   ├── poetry-card/      # 诗词卡片
│   ├── empty-state/      # 空状态
│   └── loading-state/    # 加载状态
│
├── pages/                 # 页面
│   ├── index/            # 首页（每日推荐）
│   ├── login/            # 登录页
│   ├── profile/          # 个人中心
│   ├── theme/            # 主题设置 ⭐
│   ├── poetry-list/      # 诗词列表
│   ├── poetry-detail/    # 诗词详情
│   ├── author-list/      # 作者列表
│   ├── author-detail/    # 作者详情
│   ├── square/           # 广场
│   ├── game/             # 飞花令游戏
│   ├── search/           # 搜索
│   ├── discover/         # 发现
│   ├── messages/         # 消息中心
│   └── settings/         # 设置
│
├── stores/                # 状态管理
│   ├── theme.js          # 主题状态 ⭐
│   ├── user.js           # 用户状态
│   └── poetry.js         # 诗词状态
│
├── styles/                # 全局样式
│   ├── variables.scss    # SCSS 变量
│   └── global.scss       # 全局样式
│
├── utils/                 # 工具函数
│   ├── request.js        # HTTP 请求封装
│   └── index.js          # 通用工具函数
│
├── static/                # 静态资源
│
├── App.vue               # 应用入口
├── main.js               # 主入口
├── pages.json            # 页面配置
├── manifest.json         # 应用配置
└── package.json          # 依赖配置
```

## 快速开始

### 安装依赖

```bash
cd client-app-uniapp
npm install
```

### 运行开发

```bash
# 微信小程序
npm run dev:mp-weixin

# H5
npm run dev:h5
```

### 构建生产

```bash
# 微信小程序
npm run build:mp-weixin

# H5
npm run build:h5
```

## 主题系统使用

### 在页面中使用主题

```vue
<script setup>
import { computed } from 'vue'
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()
const pageStyle = computed(() => {
  const theme = themeStore.theme
  return {
    backgroundColor: theme.bgColor,
    color: theme.textColor
  }
})
</script>

<template>
  <view :style="pageStyle">
    <!-- 页面内容 -->
  </view>
</template>
```

### 切换主题

```javascript
import { useThemeStore } from '@/stores/theme'

const themeStore = useThemeStore()

// 切换到指定主题
themeStore.setTheme('dark')

// 切换到下一个主题
themeStore.nextTheme()
```

### 可用主题列表

| 主题名称 | Key | 图标 | 说明 |
|---------|-----|------|------|
| 明亮 | light | ☀️ | 清新明快的亮色主题 |
| 暗黑 | dark | 🌙 | 深邃神秘的暗色主题 |
| 清新 | fresh | 🌿 | 春日绿意的自然主题 |
| 炫紫 | purple | 💜 | 神秘优雅的紫色主题 |
| 温馨 | warm | 🧡 | 暖橙舒适的温暖主题 |
| 海洋 | ocean | 🌊 | 深蓝宁静的海洋主题 |
| 森林 | forest | 🌲 | 墨绿深沉的森林主题 |
| 晚霞 | sunset | 🌅 | 粉橙渐变的晚霞主题 |
| 星空 | starry | ⭐ | 深蓝静谧的星空主题 |
| 简约 | minimal | ⚪ | 灰度优雅的简约主题 |

## API 对接

后端 API 地址配置在 `utils/request.js` 中：

```javascript
const BASE_URL = process.env.NODE_ENV === 'development'
  ? 'http://localhost:8000/api/v1'
  : 'https://api.xingyu-poetry.com/api/v1'
```

所有 API 接口已封装在 `api/` 目录下，支持：

- 自动添加 Authorization Token
- 统一错误处理
- 自动显示 loading
- 请求和响应拦截

## 功能清单

### 已完成功能 ✅

- [x] 项目基础结构
- [x] 主题系统（10种主题 + 过渡动画）⭐
- [x] API 封装和工具函数
- [x] 状态管理（Pinia）
- [x] 通用组件（诗词卡片、空状态、加载状态）
- [x] 首页（每日诗词推荐）
- [x] 登录页（微信登录 + 账号密码登录）
- [x] 个人中心页
- [x] 主题设置页 ⭐

### 待完善功能 📝

- [ ] 诗词列表页
- [ ] 诗词详情页
- [ ] 评论系统
- [ ] 广场页面
- [ ] 飞花令游戏
- [ ] 作者列表和详情
- [ ] 搜索页面
- [ ] 发现页面
- [ ] 消息系统
- [ ] 设置页面

## 注意事项

1. **主题系统**是项目的重点功能，已完整实现10种主题和过渡效果
2. 所有页面都需要使用主题系统，确保样式统一
3. API 接口需要后端服务支持，请确保后端服务正常运行
4. 小程序开发需要配置 `manifest.json` 中的 `appid`
5. 图片资源需要放在 `static/` 目录下

## 开发规范

### 代码注释

- 所有函数和组件都有详细的注释说明
- 关键逻辑都有行内注释
- 使用 JSDoc 格式注释

### 命名规范

- 组件：PascalCase（如：PoetryCard）
- 文件：kebab-case（如：poetry-card.vue）
- 变量和函数：camelCase（如：getUserInfo）
- 常量：UPPER_SNAKE_CASE（如：API_BASE_URL）

### 样式规范

- 使用 SCSS 变量统一管理样式
- 使用 CSS Variables 实现主题切换
- 使用 mixins 复用样式代码
- 遵循 BEM 命名规范

## 贡献指南

欢迎贡献代码！请遵循以下步骤：

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 许可证

MIT License

## 联系方式

- 项目地址：https://github.com/your-repo/xingyu-poetry
- 问题反馈：https://github.com/your-repo/xingyu-poetry/issues

---

**星语诗词** - 让诗词文化触手可及 📖✨
