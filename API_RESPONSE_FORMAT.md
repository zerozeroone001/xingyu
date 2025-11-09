# API 响应格式规范

## 统一响应格式

所有API接口统一使用以下响应格式：

### 成功响应

```json
{
  "code": 200,
  "status": true,
  "msg": "请求成功",
  "data": {
    // 实际数据
  }
}
```

### 错误响应

```json
{
  "code": 400,
  "status": false,
  "msg": "错误信息",
  "data": null
}
```

## 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| code | int | HTTP状态码，200表示成功，其他表示错误 |
| status | boolean | 请求状态，true表示成功，false表示失败 |
| msg | string | 响应消息，成功时为"请求成功"或具体操作信息，失败时为错误提示 |
| data | any | 响应数据，成功时包含实际数据，失败时为null |

## 常见状态码

| 状态码 | 说明 |
|--------|------|
| 200 | 请求成功 |
| 400 | 请求参数错误 |
| 401 | 未授权，需要登录 |
| 403 | 无权限访问 |
| 404 | 资源不存在 |
| 422 | 参数验证失败 |
| 500 | 服务器内部错误 |

## 异常处理

后端使用全局异常处理器统一所有错误响应格式，包括：

1. **HTTPException** - 认证错误、权限错误、404等HTTP异常
2. **RequestValidationError** - 参数验证错误（状态码422）
3. **Exception** - 未捕获的服务器内部错误（状态码500）

所有异常都会返回统一的错误响应格式。

## 列表数据格式

对于返回列表数据的接口，`data` 字段使用以下结构：

```json
{
  "code": 200,
  "status": true,
  "msg": "请求成功",
  "data": {
    "list": [
      // 数据项
    ],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

### 分页字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| list | array | 数据列表 |
| total | int | 总记录数 |
| page | int | 当前页码（从1开始） |
| page_size | int | 每页记录数 |
| total_pages | int | 总页数 |

## 示例

### 1. 获取用户信息（单条数据）

**请求：** `GET /api/v1/users/me`

**响应：**
```json
{
  "code": 200,
  "status": true,
  "msg": "请求成功",
  "data": {
    "id": 1,
    "username": "zhangsan",
    "nickname": "张三",
    "avatar": "https://example.com/avatar.jpg",
    "created_at": "2024-01-01T00:00:00"
  }
}
```

### 2. 获取诗词列表（列表数据）

**请求：** `GET /api/v1/poetry?page=1&page_size=20`

**响应：**
```json
{
  "code": 200,
  "status": true,
  "msg": "请求成功",
  "data": {
    "list": [
      {
        "id": 1,
        "title": "静夜思",
        "author": "李白",
        "content": "床前明月光，疑是地上霜。举头望明月，低头思故乡。"
      },
      {
        "id": 2,
        "title": "春晓",
        "author": "孟浩然",
        "content": "春眠不觉晓，处处闻啼鸟。夜来风雨声，花落知多少。"
      }
    ],
    "total": 1000,
    "page": 1,
    "page_size": 20,
    "total_pages": 50
  }
}
```

### 3. 登录失败（错误响应）

**请求：** `POST /api/v1/auth/login`

**响应：**
```json
{
  "code": 401,
  "status": false,
  "msg": "用户名或密码错误",
  "data": null
}
```

### 4. 参数错误（错误响应）

**请求：** `GET /api/v1/poetry?page=0`

**响应：**
```json
{
  "code": 400,
  "status": false,
  "msg": "页码必须大于等于1",
  "data": null
}
```

### 5. 认证失败（错误响应）

**请求：** `GET /api/v1/users/me`（未提供token）

**响应：**
```json
{
  "code": 401,
  "status": false,
  "msg": "Not authenticated",
  "data": null
}
```

### 6. 参数验证失败（错误响应）

**请求：** `POST /api/v1/auth/register`（缺少必填字段）

**响应：**
```json
{
  "code": 422,
  "status": false,
  "msg": "参数验证失败: body.username: field required; body.password: field required",
  "data": {
    "errors": [
      {
        "loc": ["body", "username"],
        "msg": "field required",
        "type": "value_error.missing"
      }
    ]
  }
}
```

注意：`data.errors` 字段仅在DEBUG模式下返回。

## 前端使用

### TypeScript 类型定义

```typescript
// 响应数据接口
export interface ApiResponse<T = any> {
  code: number;
  status: boolean;
  msg: string;
  data: T;
}

// 分页响应接口
export interface PaginationResponse<T = any> {
  list: T[];
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}
```

### 使用示例

```typescript
import { ApiResponse, PaginationResponse } from '@/utils/request';

// 获取单条数据
interface User {
  id: number;
  username: string;
  nickname: string;
}

const getUserInfo = async (): Promise<User> => {
  const response: ApiResponse<User> = await request.get('/users/me');
  if (response.code === 200 && response.status) {
    return response.data;
  }
  throw new Error(response.msg);
};

// 获取列表数据
interface Poetry {
  id: number;
  title: string;
  author: string;
  content: string;
}

const getPoetryList = async (page: number): Promise<Poetry[]> => {
  const response: ApiResponse<PaginationResponse<Poetry>> =
    await request.get('/poetry', { params: { page, page_size: 20 } });

  if (response.code === 200 && response.status) {
    return response.data.list;
  }
  throw new Error(response.msg);
};
```

## 注意事项

1. **code 字段**：使用标准HTTP状态码，200表示成功
2. **status 字段**：布尔类型，`true`表示成功，`false`表示失败
3. **msg 字段**：提供清晰的中文提示信息
4. **data 字段**：
   - 成功时包含实际数据
   - 失败时为 `null`
   - 列表数据时，`data` 是一个包含 `list` 和分页信息的对象
5. **列表字段名**：统一使用 `list`（而不是 `items`）
6. **分页字段名**：统一使用 `page_size`（而不是 `size`）和 `total_pages`（而不是 `pages`）

## 迁移说明

### 从旧格式迁移

**旧格式：**
```json
{
  "code": 0,
  "message": "success",
  "data": {
    "items": [],
    "total": 100
  }
}
```

**新格式：**
```json
{
  "code": 200,
  "status": true,
  "msg": "请求成功",
  "data": {
    "list": [],
    "total": 100,
    "page": 1,
    "page_size": 20,
    "total_pages": 5
  }
}
```

### 主要变更

1. `code: 0` → `code: 200`
2. `message` → `msg`
3. 添加 `status` 字段
4. `items` → `list`
5. `size` → `page_size`
6. `pages` → `total_pages`
