# Backend Design

## 1. 目标

`backend` 为微信小程序提供诗词内容、用户登录、收藏历史、广场互动和飞花令玩法 API。第一版以可联调、可启动、可扩展为目标，不做管理后台、排行榜、成就系统和复杂搜索排序。

## 2. 技术选型

| 模块 | 选型 | 说明 |
| --- | --- | --- |
| Web 框架 | FastAPI | REST API 与 OpenAPI 文档 |
| 数据库 | SQLite | 本地轻量部署，后续可迁移 MySQL/PostgreSQL |
| ORM | SQLAlchemy | 管理模型、索引和查询 |
| Schema | Pydantic | 入参和出参校验 |
| 鉴权 | Bearer JWT | 小程序保存 token，后端校验用户身份 |
| 缓存 | 本地 TTL 缓存 | 先覆盖首页、分类、详情、关键词等读多数据 |
| 运行 | uvicorn | 本地开发和部署启动 |

## 3. 目录规划

```text
backend/
  app/
    main.py
    api/v1/
    core/
    db/
    schemas/
    services/
    utils/
  tests/
  requirements.txt
  README.md
```

## 4. API 约定

所有接口使用 `/api/v1` 前缀，响应格式统一为：

```json
{
  "code": 0,
  "message": "success",
  "data": {}
}
```

分页响应统一为：

```json
{
  "items": [],
  "page": 1,
  "page_size": 10,
  "total": 0,
  "has_more": false
}
```

鉴权接口使用请求头：

```http
Authorization: Bearer <token>
```

## 5. API 契约

| 模块 | 方法 | 路径 | 登录 | 说明 |
| --- | --- | --- | --- | --- |
| 健康检查 | GET | `/health` | 否 | 服务状态 |
| 登录 | POST | `/auth/wx-login` | 否 | 微信 code 登录，开发环境允许 mock |
| 登录 | POST | `/auth/logout` | 是 | 退出登录 |
| 用户 | GET | `/users/me` | 是 | 当前用户 |
| 用户 | PUT | `/users/me` | 是 | 更新昵称、头像、资料 |
| 用户 | GET | `/users/me/overview` | 是 | 个人中心概览 |
| 用户 | GET | `/users/me/{type}` | 是 | 个人列表，`poems`、`likes`、`favorites`、`follows` |
| 首页 | GET | `/home` | 否 | 首页聚合数据 |
| 诗词 | GET | `/poems` | 否 | 诗词列表 |
| 诗词 | GET | `/poems/search` | 否 | 按标题、作者、正文搜索 |
| 诗词 | GET | `/poems/{poem_id}` | 否 | 诗词详情 |
| 分类 | GET | `/categories` | 否 | 分类列表 |
| 分类 | GET | `/categories/{category_id}/poems` | 否 | 分类下诗词 |
| 收藏 | GET | `/favorites` | 是 | 我的收藏 |
| 收藏 | POST | `/favorites/{poem_id}` | 是 | 收藏诗词 |
| 收藏 | DELETE | `/favorites/{poem_id}` | 是 | 取消收藏 |
| 历史 | GET | `/history` | 是 | 浏览历史 |
| 历史 | POST | `/history/{poem_id}` | 是 | 记录浏览 |
| 广场 | GET | `/square/feed` | 否 | 内容流 |
| 广场 | POST | `/square/feed` | 是 | 发布内容 |
| 广场 | GET | `/square/feed/{topic_id}` | 否 | 内容详情 |
| 广场 | POST | `/square/feed/{topic_id}/like` | 是 | 切换点赞 |
| 广场 | POST | `/square/feed/{topic_id}/favorite` | 是 | 切换收藏 |
| 广场 | POST | `/square/feed/{topic_id}/share` | 否 | 分享计数 |
| 广场 | POST | `/square/feed/{topic_id}/comments` | 是 | 新增评论 |
| 广场 | POST | `/square/feed/{topic_id}/comments/{comment_id}/like` | 是 | 评论点赞 |
| 广场 | POST | `/square/feed/{topic_id}/comments/{comment_id}/favorite` | 是 | 评论收藏 |
| 飞花令 | GET | `/feihualing/keywords` | 否 | 关键词列表 |
| 飞花令 | POST | `/feihualing/check` | 否 | 校验答案 |
| 飞花令 | GET | `/feihualing/records` | 是 | 我的记录 |
| 飞花令 | POST | `/feihualing/records` | 是 | 保存记录 |
| 飞花令 | GET | `/feihualing/rooms` | 否 | 房间列表 |
| 飞花令 | POST | `/feihualing/rooms` | 是 | 创建房间 |
| 飞花令 | GET | `/feihualing/rooms/{room_id}` | 否 | 房间详情 |
| 反馈 | POST | `/feedback` | 否 | 提交反馈 |

## 6. 表结构

### users

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | INTEGER PK | 用户 ID |
| openid | TEXT UNIQUE | 微信 openid 或开发 mock openid |
| nickname | TEXT | 昵称 |
| avatar_url | TEXT | 头像 |
| avatar_text | TEXT | 头像占位字 |
| title | TEXT | 个人称号 |
| level | INTEGER | 等级 |
| gender | TEXT | 性别 |
| city | TEXT | 城市 |
| bio | TEXT | 简介 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### poems

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | INTEGER PK | 诗词 ID |
| title | TEXT | 标题 |
| dynasty | TEXT | 朝代 |
| author | TEXT | 作者 |
| content | TEXT | 正文 |
| recommend_sentence | TEXT | 推荐句 |
| tags | TEXT | JSON 字符串 |
| like_count | INTEGER | 点赞数 |
| favorite_count | INTEGER | 收藏数 |
| share_count | INTEGER | 分享数 |
| created_at | DATETIME | 创建时间 |
| updated_at | DATETIME | 更新时间 |

### poem_names

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| id | INTEGER PK | 名称 ID |
| name | TEXT | 诗词名称 |

当前开发库通过 `python -m app.db.import_poetry` 导入内容数据：唐诗 300、宋词 200、元曲 200、明代诗词 30、清词 200，共 930 条；`poem_names` 同步保存 930 条名称。

### categories / poem_categories

`categories` 保存分类名称、类型、排序；`poem_categories` 保存诗词与分类多对多关系。`GET /categories` 会返回每个分类下的 `poem_count` / `poemCount`，供分类页展示数量。

### favorites / browse_history

`favorites` 使用 `user_id + poem_id` 唯一索引避免重复收藏；`browse_history` 使用 `user_id + poem_id` 唯一索引，重复浏览时更新 `viewed_at`。

### square_topics / square_comments / square_reactions

广场内容、评论和点赞收藏关系拆开保存。`square_reactions` 通过 `target_type` 区分 `topic` 和 `comment`，通过 `reaction_type` 区分 `like` 和 `favorite`。

### feihualing_records / feihualing_rooms / feihualing_room_messages

飞花令记录保存答题结果；房间和消息用于后续多人玩法，第一版先提供可联调数据结构。

### feedback

保存用户反馈内容、联系方式和处理状态。

## 7. 缓存策略

| Key | TTL | 说明 |
| --- | --- | --- |
| `home:data` | 300 秒 | 首页聚合 |
| `poem:detail:{id}` | 1800 秒 | 诗词详情 |
| `category:list` | 1800 秒 | 分类列表 |
| `category:poems:{id}:{page}:{page_size}` | 600 秒 | 分类诗词 |
| `square:feed:{page}:{page_size}` | 300 秒 | 广场内容流 |
| `feihualing:keywords` | 1800 秒 | 飞花令关键词 |

写操作成功后清理相关前缀，例如收藏后清理 `poem:detail:` 和用户收藏列表。

## 8. 阶段任务

### 阶段一：基础工程

1. 新建 FastAPI 工程。
2. 配置 SQLite、SQLAlchemy、统一响应、异常处理、鉴权。
3. 建立模型、schema、分页工具和本地缓存。
4. 提供种子数据脚本，服务启动时可初始化开发数据。

### 阶段二：内容接口

1. 实现首页、诗词列表、详情、搜索。
2. 实现分类列表和分类诗词。
3. 支持收藏状态随登录用户变化。

### 阶段三：用户接口

1. 实现 mock 微信登录和真实微信登录扩展点。
2. 实现个人资料、概览、收藏、历史。
3. 接入小程序登录态失效处理。

### 阶段四：互动接口

1. 实现广场内容流、发布、点赞、收藏、评论。
2. 实现飞花令关键词、答案校验、记录。
3. 实现飞花令房间的基础查询和创建。

### 阶段五：联调与验收

1. 将小程序 `useMock` 切到 `false`。
2. 对齐所有 service 的字段名。
3. 验证 `/docs`、SQLite 初始化、核心页面数据流。
4. 补充接口测试和业务边界测试。
