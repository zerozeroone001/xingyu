# 数据导入脚本

本目录包含诗词平台的数据导入工具和示例数据。

## 文件说明

- `import_poetry.py` - 诗词数据导入脚本
- `sample_data.json` - 示例诗词数据（包含5位作者和10首诗词）

## 使用方法

### 1. 准备数据库

确保MySQL数据库已启动并且已经执行了数据库迁移：

```bash
# 启动数据库（如果使用docker-compose）
cd /home/user/xingyu/server
docker-compose up -d mysql

# 执行数据库迁移
alembic upgrade head
```

### 2. 配置环境变量

确保 `.env` 文件中的数据库连接配置正确：

```env
DATABASE_URL=mysql+aiomysql://root:password@localhost:3306/xingyu_poetry?charset=utf8mb4
```

### 3. 运行导入脚本

```bash
# 进入server目录
cd /home/user/xingyu/server

# 运行导入脚本
python scripts/import_poetry.py
```

## 示例数据说明

### 作者数据（5位）

1. **李白**（唐代）- 诗仙，浪漫主义诗人
2. **杜甫**（唐代）- 诗圣，现实主义诗人
3. **白居易**（唐代）- 诗魔/诗王
4. **王维**（唐代）- 诗佛，山水田园诗人
5. **苏轼**（宋代）- 豪放派词人

### 诗词数据（10首）

- 李白：《静夜思》《将进酒》
- 杜甫：《春望》《登高》
- 白居易：《琵琶行》
- 王维：《相思》《山居秋暝》《九月九日忆山东兄弟》
- 苏轼：《水调歌头·明月几时有》《念奴娇·赤壁怀古》

每首诗词包含：
- 标题、内容、作者
- 朝代、类型、标签
- 翻译、注释、赏析

## 导入特性

- ✅ 自动检查重复数据，避免重复导入
- ✅ 支持部分导入，已存在的数据会自动跳过
- ✅ 事务处理，导入失败自动回滚
- ✅ 详细的导入进度和统计信息

## 扩展数据源

如需导入更多数据，可以：

1. **修改 sample_data.json**：按照现有格式添加更多作者和诗词
2. **使用其他数据源**：如 [chinese-poetry](https://github.com/chinese-poetry/chinese-poetry) 项目
3. **编写自定义导入脚本**：参考 `import_poetry.py` 的实现

## 注意事项

- 导入前请确保数据库表结构已经创建（运行 `alembic upgrade head`）
- ID字段会保持原值，请确保不同数据源的ID不会冲突
- 标签字段为JSON数组格式：`["标签1", "标签2"]`
- 诗词状态默认为 1（已发布）
