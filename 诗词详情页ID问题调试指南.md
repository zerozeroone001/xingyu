# 诗词详情页ID问题调试指南

## 问题描述

用户端首页点击诗词跳转到详情页时，API接口 `/api/v1/poetries/768595412145755100` 返回"诗词不存在"。

## 问题分析

通过代码分析，发现以下关键点：

### 1. 数据库ID类型
- 诗词表使用 `BigInteger` 类型作为主键 (`server/app/models/poetry.py:18`)
- 支持超大整数ID（如雪花ID）

### 2. 前端ID处理
- 诗词详情页使用 `parseInt()` 处理URL参数 (`client-app/src/pages/poetry-detail/poetry-detail.vue:323`)
- JavaScript的 `Number.MAX_SAFE_INTEGER` = 9007199254740991
- ID `768595412145755100` < `MAX_SAFE_INTEGER`，理论上不会精度丢失

### 3. 示例数据
- `server/scripts/sample_data.json` 中的ID是简单数字：1, 2, 3, 4, 5...
- 报告的ID `768595412145755100` 远大于示例数据范围

## 诊断步骤

### 步骤1：检查数据库中的实际诗词ID

#### 方法A：使用调试API（推荐）

启动后端服务后，访问：
```
http://localhost:8000/api/v1/poetries/debug/ids?limit=20
```

这个接口会返回数据库中前20条诗词的ID、标题和状态。

示例响应：
```json
{
  "code": 200,
  "msg": "success",
  "data": [
    {"id": 1, "title": "静夜思", "status": 1},
    {"id": 2, "title": "将进酒", "status": 1},
    ...
  ]
}
```

#### 方法B：直接查询数据库

如果使用Docker：
```bash
docker exec -it poetry-mysql mysql -uroot -proot123 poetry -e "SELECT id, title, status FROM poetries ORDER BY id LIMIT 20;"
```

如果使用本地MySQL：
```bash
mysql -uroot -p poetry -e "SELECT id, title, status FROM poetries ORDER BY id LIMIT 20;"
```

### 步骤2：检查前端获取的诗词ID

1. 打开浏览器开发者工具（F12）
2. 切换到 Console 标签
3. 访问首页 `http://localhost:8080` 或 `http://localhost:5173`
4. 查看控制台输出，重点关注：
   - `每日推荐API响应 data`：查看API返回的原始数据
   - `每日诗词ID` 和类型：查看解析后的ID值
   - 点击诗词时的日志：`点击的诗词ID` 和 `当前诗词对象`

### 步骤3：对比分析

对比数据库中的ID和前端获取到的ID：
- **如果ID一致**：问题可能在API路由或查询逻辑
- **如果ID不一致**：问题在数据生成或传递过程

## 可能的原因和解决方案

### 原因1：数据库中确实没有这个ID的诗词

**检查方法**：
查询数据库中是否存在ID为 `768595412145755100` 的诗词：
```sql
SELECT * FROM poetries WHERE id = 768595412145755100;
```

**解决方案**：
如果诗词不存在，需要检查：
1. 诗词数据是否已导入？运行 `python scripts/import_poetry.py`
2. 数据导入时ID生成策略是否正确？
3. 是否使用了自动生成的ID而不是JSON中的固定ID？

### 原因2：诗词状态不是"已发布"

**检查方法**：
查询诗词的状态：
```sql
SELECT id, title, status FROM poetries WHERE id = 768595412145755100;
```

状态值说明：
- 1 = 已发布
- 2 = 草稿
- 3 = 已删除

**解决方案**：
如果诗词存在但status不是1，更新状态：
```sql
UPDATE poetries SET status = 1 WHERE id = 768595412145755100;
```

### 原因3：ID生成策略配置错误

**检查方法**：
查看数据库表结构：
```sql
SHOW CREATE TABLE poetries;
```

查看ID列是否配置了自动生成（如AUTO_INCREMENT）。

**解决方案**：
如果使用自动生成ID：
- 确保插入时不指定ID，让数据库自动生成
- 或者使用雪花ID等分布式ID生成器

如果使用固定ID：
- 确保JSON数据中的ID与数据库一致
- 导入时使用JSON中的ID值

### 原因4：前端mock数据干扰

**检查方法**：
查看 `client-app/src/pages/index/index.vue:161` 的 `useMockData` 变量。

**解决方案**：
确保 `useMockData = false`，使用真实API而不是mock数据。

## 快速修复方案

### 方案A：使用简单自增ID（推荐）

修改 `server/scripts/import_poetry.py`，在导入时不指定ID：

```python
# 修改前
poetry = Poetry(
    id=poetry_data["id"],  # ← 移除这行
    title=...
)

# 修改后
poetry = Poetry(
    # id会自动生成
    title=...
)
```

然后重新导入数据：
```bash
# 清空现有数据
mysql -uroot -p poetry -e "TRUNCATE TABLE poetries;"

# 重新导入
cd server
python scripts/import_poetry.py
```

### 方案B：将ID作为字符串处理

如果必须使用超大ID，将ID作为字符串在前后端传递：

1. **后端** - 修改Schema (`server/app/schemas/poetry.py`):
```python
class PoetryBase(BaseModel):
    # 其他字段...
    pass

class PoetryDetail(PoetryBase):
    id: str = Field(..., description="诗词ID")  # int → str
    # 其他字段...
```

2. **前端** - 修改类型定义和处理:
```typescript
// client-app/src/api/poetry.ts
export interface Poetry {
  id: string;  // number → string
  // 其他字段...
}

// client-app/src/pages/poetry-detail/poetry-detail.vue
const poetryId = ref<string>('');  // number → string
const id = getQueryParam('id');
if (id) {
  poetryId.value = id;  // 不再使用 parseInt
  loadPoetryDetail();
}
```

## 验证修复

修复后，执行以下验证：

1. **后端验证**：
```bash
curl http://localhost:8000/api/v1/poetries/debug/ids?limit=5
```
确认返回的ID格式正确。

2. **前端验证**：
- 访问首页
- 查看控制台日志，确认API返回的ID正确
- 点击诗词卡片
- 确认能正常跳转到详情页且加载成功

3. **详情页直接访问**：
使用调试API获取的真实ID，直接访问：
```
http://localhost:8080/poetry-detail?id=1
```

## 后续优化建议

1. **统一ID类型**：
   - 如果使用自增ID，改为INT类型
   - 如果使用分布式ID，确保前后端都作为字符串处理

2. **添加错误处理**：
   - 详情页增加友好的错误提示
   - 区分"诗词不存在"和"未发布"的情况

3. **数据一致性检查**：
   - 添加数据验证脚本
   - 定期检查诗词状态

4. **日志记录**：
   - 记录访问不存在的诗词ID
   - 便于发现数据问题

## 联系支持

如果按照以上步骤仍无法解决问题，请提供：
1. 调试API的完整响应
2. 浏览器控制台的完整日志
3. 数据库查询结果

以便进一步分析。
