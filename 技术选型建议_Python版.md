# 诗词程序 - 技术选型建议（Python后端 + AI集成）

## 一、技术选型对比分析

### 1.1 前端框架选型

#### 用户端（小程序 + H5）

| 技术方案 | 优点 | 缺点 | 适用场景 | 推荐指数 |
|---------|------|------|---------|---------|
| **uni-app** | - 一套代码多端运行（小程序+H5+APP）<br>- Vue语法，学习成本低<br>- 社区活跃，插件丰富<br>- 官方维护，更新及时 | - 性能略逊于原生<br>- 某些特殊功能需要条件编译<br>- 可能遇到平台兼容性问题 | **多端需求、快速开发** | ⭐⭐⭐⭐⭐ |
| **Taro** | - React/Vue语法可选<br>- 京东团队维护<br>- 多端支持<br>- TypeScript支持好 | - 学习成本相对较高<br>- 部分API需要适配<br>- 社区不如uni-app | React技术栈团队 | ⭐⭐⭐⭐ |
| **原生小程序 + Vue H5** | - 小程序性能最优<br>- 功能最完整<br>- 官方支持最好 | - 需要维护两套代码<br>- 开发成本高<br>- 代码复用困难 | 对性能要求极高的项目 | ⭐⭐⭐ |

**推荐方案：uni-app**

**理由**：
1. 一套代码同时支持小程序和H5，大幅降低开发成本
2. Vue语法简单易学，开发效率高
3. 社区活跃，问题容易解决
4. 未来如需扩展APP，成本较低

---

#### 管理端

| 技术方案 | 优点 | 缺点 | 推荐指数 |
|---------|------|------|---------|
| **Vue 3 + Element Plus** | - 组件丰富<br>- 中文文档完善<br>- 上手快<br>- 适合后台系统 | - Element Plus相对较新 | ⭐⭐⭐⭐⭐ |
| **Vue 3 + Ant Design Vue** | - 组件质量高<br>- 设计规范<br>- 企业级UI | - 文档相对简单 | ⭐⭐⭐⭐⭐ |
| **React + Ant Design** | - 生态最成熟<br>- 企业级解决方案<br>- 性能优秀 | - 学习曲线陡峭<br>- 需要掌握React生态 | ⭐⭐⭐⭐ |

**推荐方案：Vue 3 + Element Plus**

---

### 1.2 后端框架选型（Python）⭐ 重点

| 技术方案 | 优点 | 缺点 | 适用场景 | 推荐指数 |
|---------|------|------|---------|---------|
| **FastAPI** | - **性能最优**（接近Node.js/Go）<br>- **自动生成OpenAPI文档**<br>- **原生支持异步**<br>- **类型提示，自动验证**<br>- **易于集成AI模型**<br>- 现代化Python框架 | - 相对较新<br>- 社区不如Flask/Django | **API服务、AI项目、高性能** | ⭐⭐⭐⭐⭐ |
| **Django + DRF** | - 功能最全（自带ORM、Admin）<br>- 生态最成熟<br>- 文档完善<br>- 适合大型项目 | - 重量级，启动慢<br>- 学习曲线陡<br>- 不适合异步 | 企业级大型项目 | ⭐⭐⭐⭐ |
| **Flask** | - 轻量灵活<br>- 学习成本低<br>- 扩展丰富 | - 需要自己组织架构<br>- 异步支持一般<br>- 性能一般 | 小型项目、快速原型 | ⭐⭐⭐ |
| **Tornado** | - 异步支持好<br>- 适合长连接 | - 生态较小<br>- 学习成本高 | WebSocket密集型应用 | ⭐⭐⭐ |
| **Sanic** | - 异步高性能<br>- 类Flask语法 | - 生态较小<br>- 不够稳定 | 高性能API | ⭐⭐⭐ |

**推荐方案：FastAPI（强烈推荐）**

#### FastAPI 详细优势分析

##### 1. 性能卓越
```python
# 性能对比（请求/秒）
FastAPI (Uvicorn): ~20,000+ req/s
Django: ~2,000 req/s
Flask: ~1,500 req/s
Node.js (Express): ~25,000 req/s
```

FastAPI基于Starlette和Pydantic，性能接近Node.js，是Django的10倍！

##### 2. 自动文档生成
```python
# 只需要定义API，自动生成Swagger UI和ReDoc文档
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    """创建用户"""
    return user

# 访问 /docs 即可看到交互式API文档
# 访问 /redoc 可以看到更详细的文档
```

##### 3. 类型安全与自动验证
```python
from pydantic import BaseModel, Field

class PoetryCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)
    author_id: int = Field(..., gt=0)
    dynasty: str

    class Config:
        json_schema_extra = {
            "example": {
                "title": "静夜思",
                "content": "床前明月光...",
                "author_id": 1,
                "dynasty": "唐代"
            }
        }

@app.post("/poetry/")
async def create_poetry(poetry: PoetryCreate):
    # 如果参数不符合类型，自动返回详细错误信息
    # 无需手动验证，Pydantic自动处理
    return poetry
```

##### 4. 原生异步支持
```python
# 支持异步数据库查询
@app.get("/poetry/{poetry_id}")
async def get_poetry(poetry_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(Poetry).where(Poetry.id == poetry_id)
    )
    return result.scalar_one_or_none()

# 支持异步HTTP请求
@app.get("/recommend/{user_id}")
async def get_recommendation(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"http://ai-service/recommend/{user_id}")
        return response.json()
```

##### 5. 依赖注入系统
```python
from fastapi import Depends

# 数据库依赖
async def get_db():
    async with AsyncSession() as session:
        yield session

# 用户认证依赖
async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = verify_token(token)
    if not user:
        raise HTTPException(status_code=401)
    return user

# 在路由中使用
@app.get("/profile/")
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    return current_user
```

##### 6. 完美集成AI模型 🔥

**这是选择Python的核心原因！**

```python
from transformers import pipeline
import torch

# 在FastAPI中加载AI模型
class AIService:
    def __init__(self):
        # 诗词生成模型
        self.poetry_generator = pipeline(
            "text-generation",
            model="gpt2-chinese-poetry"
        )

        # 文本分类模型（诗词朝代分类）
        self.dynasty_classifier = pipeline(
            "text-classification",
            model="bert-base-chinese"
        )

        # 情感分析模型
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="chinese-roberta-sentiment"
        )

    async def generate_poetry(self, prompt: str, style: str):
        """AI生成诗词"""
        result = self.poetry_generator(
            prompt,
            max_length=100,
            num_return_sequences=1
        )
        return result[0]['generated_text']

    async def classify_dynasty(self, poetry: str):
        """识别诗词朝代"""
        result = self.dynasty_classifier(poetry)
        return result[0]['label']

    async def analyze_sentiment(self, text: str):
        """分析诗词情感"""
        result = self.sentiment_analyzer(text)
        return result[0]

# 在API中使用
ai_service = AIService()

@app.post("/ai/generate-poetry")
async def generate_poetry(request: PoetryGenerateRequest):
    poetry = await ai_service.generate_poetry(
        request.prompt,
        request.style
    )
    return {"poetry": poetry}

@app.post("/ai/classify")
async def classify_poetry(poetry: str):
    dynasty = await ai_service.classify_dynasty(poetry)
    return {"dynasty": dynasty}
```

---

### 1.3 Python ORM框架选型

| ORM | 优点 | 缺点 | 推荐指数 |
|-----|------|------|---------|
| **SQLAlchemy 2.0** | - **最成熟的Python ORM**<br>- **支持异步**（2.0版本）<br>- 功能强大<br>- 与FastAPI集成好 | - 学习曲线稍陡 | ⭐⭐⭐⭐⭐ |
| **Tortoise ORM** | - 类似Django ORM<br>- 原生异步<br>- 简单易用 | - 功能不如SQLAlchemy<br>- 社区较小 | ⭐⭐⭐⭐ |
| **Django ORM** | - 最简单<br>- 功能完整 | - 只能用于Django<br>- 不支持异步 | ⭐⭐⭐ |
| **Peewee** | - 轻量简洁<br>- 学习成本低 | - 功能有限<br>- 不支持异步 | ⭐⭐⭐ |

**推荐方案：SQLAlchemy 2.0**

**示例代码**：
```python
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# 创建异步引擎
engine = create_async_engine(
    "mysql+aiomysql://user:pass@localhost/poetry_db",
    echo=True
)

# 创建异步Session
async_session = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

Base = declarative_base()

# 定义模型
class Poetry(Base):
    __tablename__ = "poetry"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text, nullable=False)
    author_id = Column(Integer, ForeignKey("authors.id"))
    dynasty = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    author = relationship("Author", back_populates="poetries")
    comments = relationship("Comment", back_populates="poetry")

# 异步查询
async def get_poetry(poetry_id: int):
    async with async_session() as session:
        result = await session.execute(
            select(Poetry).where(Poetry.id == poetry_id)
        )
        return result.scalar_one_or_none()
```

---

### 1.4 数据库选型

#### 关系型数据库

| 数据库 | 优点 | 缺点 | 推荐指数 |
|--------|------|------|---------|
| **MySQL 8.0** | - 开源免费<br>- 生态成熟<br>- 性能优秀<br>- 社区活跃<br>- JSON支持 | - 复杂查询不如PostgreSQL | ⭐⭐⭐⭐⭐ |
| **PostgreSQL** | - 功能最强大<br>- JSON/JSONB支持最好<br>- 适合复杂查询<br>- 扩展丰富 | - 学习成本略高<br>- 运维稍复杂 | ⭐⭐⭐⭐⭐ |

**推荐方案：MySQL 8.0（首选）或 PostgreSQL（备选）**

对于诗词项目，MySQL 8.0足够使用。如果需要复杂的JSON查询或全文搜索，可以考虑PostgreSQL。

---

#### NoSQL数据库

| 数据库 | 用途 | 推荐指数 |
|--------|------|---------|
| **Redis** | 缓存、会话、排行榜、计数器 | ⭐⭐⭐⭐⭐ |
| **Elasticsearch** | 全文搜索、日志分析 | ⭐⭐⭐⭐⭐ |
| **MongoDB** | 非结构化数据、日志存储 | ⭐⭐⭐ |

**推荐方案：Redis + Elasticsearch**

---

### 1.5 实时通信方案（WebSocket）

| 方案 | 优点 | 缺点 | Python库 | 推荐指数 |
|------|------|------|---------|---------|
| **FastAPI WebSocket** | - 原生支持<br>- 简单易用<br>- 异步高效 | - 功能基础 | 内置 | ⭐⭐⭐⭐⭐ |
| **Socket.IO (python-socketio)** | - 功能丰富<br>- 自动降级<br>- 房间管理 | - 需要额外依赖 | python-socketio | ⭐⭐⭐⭐ |
| **Django Channels** | - Django官方方案<br>- 功能完整 | - 仅适用Django | channels | ⭐⭐⭐ |

**推荐方案：FastAPI内置WebSocket**

**示例代码**：
```python
from fastapi import WebSocket, WebSocketDisconnect

class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[int, list[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, room_id: int):
        await websocket.accept()
        if room_id not in self.active_connections:
            self.active_connections[room_id] = []
        self.active_connections[room_id].append(websocket)

    async def broadcast(self, message: dict, room_id: int):
        if room_id in self.active_connections:
            for connection in self.active_connections[room_id]:
                await connection.send_json(message)

manager = ConnectionManager()

@app.websocket("/ws/game/{room_id}")
async def game_websocket(websocket: WebSocket, room_id: int):
    await manager.connect(websocket, room_id)
    try:
        while True:
            data = await websocket.receive_json()
            # 处理飞花令游戏逻辑
            await manager.broadcast({
                "type": "game_update",
                "data": data
            }, room_id)
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_id)
```

---

### 1.6 任务队列

| 方案 | 优点 | 缺点 | 推荐指数 |
|------|------|------|---------|
| **Celery + Redis** | - 最成熟<br>- 功能最全<br>- 支持定时任务 | - 配置复杂 | ⭐⭐⭐⭐⭐ |
| **RQ (Redis Queue)** | - 简单轻量<br>- 易于使用 | - 功能较少 | ⭐⭐⭐⭐ |
| **Dramatiq** | - 现代化<br>- 性能好 | - 社区较小 | ⭐⭐⭐ |

**推荐方案：Celery**

**用途**：
- 异步发送通知
- 定时任务（每日推荐诗词）
- AI模型推理（避免阻塞API）
- 数据统计分析

**示例**：
```python
from celery import Celery

celery_app = Celery(
    "poetry",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

@celery_app.task
def generate_daily_recommendation():
    """每日生成推荐诗词（定时任务）"""
    # AI推荐逻辑
    pass

@celery_app.task
def analyze_poetry_sentiment(poetry_id: int):
    """异步分析诗词情感"""
    # AI情感分析
    pass

# 定时任务配置
celery_app.conf.beat_schedule = {
    'daily-recommendation': {
        'task': 'generate_daily_recommendation',
        'schedule': crontab(hour=6, minute=0),  # 每天早上6点
    },
}
```

---

## 二、最终推荐技术栈 🎯

### ⭐ Python AI版技术栈（强烈推荐）

```
┌─────────────────────────────────────────────────┐
│                   前端层                         │
├─────────────────────────────────────────────────┤
│  小程序+H5: uni-app (Vue 3 + TypeScript)        │
│  管理端: Vue 3 + Element Plus + TypeScript      │
└─────────────────────────────────────────────────┘
                      ↓ API请求
┌─────────────────────────────────────────────────┐
│                  后端层 (Python)                 │
├─────────────────────────────────────────────────┤
│  框架: FastAPI (Python 3.11+)                   │
│  ORM: SQLAlchemy 2.0 (异步)                     │
│  认证: JWT (python-jose)                        │
│  实时通信: FastAPI WebSocket                    │
│  任务队列: Celery + Redis                       │
│  🤖 AI引擎: PyTorch + Transformers              │
└─────────────────────────────────────────────────┘
                      ↓ 数据访问
┌─────────────────────────────────────────────────┐
│                   数据层                         │
├─────────────────────────────────────────────────┤
│  MySQL 8.0 (主数据库)                           │
│  Redis 6+ (缓存、会话、消息队列)                │
│  Elasticsearch 7+ (全文搜索)                    │
│  MinIO/OSS (对象存储 - 模型文件、图片)          │
└─────────────────────────────────────────────────┘
                      ↓ AI模型层
┌─────────────────────────────────────────────────┐
│                  AI/ML 层                        │
├─────────────────────────────────────────────────┤
│  🤖 诗词生成: GPT-2中文/千问模型                │
│  🎯 智能推荐: 协同过滤 + 内容推荐               │
│  📊 情感分析: RoBERTa中文情感模型               │
│  🏷️ 朝代分类: BERT文本分类                      │
│  🔍 语义搜索: Sentence-BERT                     │
│  🖼️ 图像识别: OCR识别古诗词图片                │
└─────────────────────────────────────────────────┘
                      ↓ 部署
┌─────────────────────────────────────────────────┐
│                   基础设施                       │
├─────────────────────────────────────────────────┤
│  容器化: Docker + Docker Compose                │
│  反向代理: Nginx                                │
│  模型服务: TorchServe / BentoML (可选)          │
│  GPU支持: NVIDIA CUDA (训练/推理加速)           │
│  对象存储: 阿里云OSS / MinIO                    │
│  CDN: 阿里云CDN / 腾讯云CDN                     │
└─────────────────────────────────────────────────┘
```

---

## 三、AI功能规划 🤖

### 3.1 核心AI功能

#### 1. 智能诗词推荐 🎯

**技术方案**：协同过滤 + 内容推荐 + 深度学习

```python
class RecommendationEngine:
    """智能推荐引擎"""

    def __init__(self):
        # 用户协同过滤模型
        self.user_cf_model = self.load_user_cf_model()

        # 内容推荐模型（基于诗词特征）
        self.content_model = self.load_content_model()

        # 深度学习推荐模型
        self.deep_model = self.load_deep_model()

    async def recommend_for_user(self, user_id: int, limit: int = 10):
        """为用户推荐诗词"""
        # 1. 获取用户历史行为
        user_history = await self.get_user_history(user_id)

        # 2. 协同过滤推荐（找相似用户喜欢的诗词）
        cf_recommendations = self.user_cf_model.predict(user_id)

        # 3. 内容推荐（基于用户喜欢的诗词特征）
        content_recommendations = self.content_model.recommend(user_history)

        # 4. 深度学习推荐（考虑多种特征）
        deep_recommendations = self.deep_model.predict(user_id)

        # 5. 融合多种推荐结果
        final_recommendations = self.merge_recommendations(
            cf_recommendations,
            content_recommendations,
            deep_recommendations
        )

        return final_recommendations[:limit]
```

**特征维度**：
- 用户行为：浏览历史、点赞、收藏、评论
- 诗词特征：朝代、作者、类型、主题、情感
- 时间因素：时间段、节日
- 社交因素：好友喜好、热门趋势

---

#### 2. AI诗词生成 ✍️

**技术方案**：GPT-2中文 / 通义千问 / ChatGLM

```python
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

class PoetryGenerator:
    """AI诗词生成器"""

    def __init__(self):
        # 加载预训练模型
        self.tokenizer = AutoTokenizer.from_pretrained("gpt2-chinese-poetry")
        self.model = AutoModelForCausalLM.from_pretrained("gpt2-chinese-poetry")
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model.to(self.device)

    async def generate_poetry(
        self,
        prompt: str,
        style: str = "五言绝句",
        dynasty: str = "唐代",
        max_length: int = 100
    ) -> str:
        """
        生成诗词

        Args:
            prompt: 主题/首句
            style: 诗词风格（五言绝句、七言律诗等）
            dynasty: 朝代风格
            max_length: 最大长度

        Returns:
            生成的诗词
        """
        # 构造输入
        input_text = f"[{dynasty}][{style}]{prompt}"
        input_ids = self.tokenizer.encode(input_text, return_tensors="pt")
        input_ids = input_ids.to(self.device)

        # 生成
        with torch.no_grad():
            output = self.model.generate(
                input_ids,
                max_length=max_length,
                num_return_sequences=1,
                no_repeat_ngram_size=2,
                top_k=50,
                top_p=0.95,
                temperature=0.8,
                do_sample=True
            )

        # 解码
        generated_text = self.tokenizer.decode(output[0], skip_special_tokens=True)

        # 后处理（去除提示词，格式化）
        poetry = self.post_process(generated_text, style)

        return poetry

    def post_process(self, text: str, style: str) -> str:
        """后处理生成的诗词"""
        # 根据style格式化（添加换行、标点等）
        if "绝句" in style:
            # 四句诗，每句换行
            lines = [text[i:i+5] for i in range(0, 20, 5)]
            return "\n".join(lines)
        # ... 其他格式
        return text

# 在API中使用
poetry_generator = PoetryGenerator()

@app.post("/ai/generate")
async def generate_poetry(request: PoetryGenerateRequest):
    """AI生成诗词"""
    poetry = await poetry_generator.generate_poetry(
        prompt=request.prompt,
        style=request.style,
        dynasty=request.dynasty
    )
    return {
        "poetry": poetry,
        "prompt": request.prompt,
        "style": request.style
    }
```

**应用场景**：
- 用户输入主题，AI创作诗词
- 续写诗句
- 飞花令AI对手
- 诗词改写/仿写

---

#### 3. 诗词情感分析 😊😢

**技术方案**：RoBERTa中文情感模型

```python
from transformers import pipeline

class SentimentAnalyzer:
    """诗词情感分析"""

    def __init__(self):
        self.analyzer = pipeline(
            "sentiment-analysis",
            model="hfl/chinese-roberta-wwm-ext-large"
        )

    async def analyze(self, poetry: str) -> dict:
        """
        分析诗词情感

        Returns:
            {
                "emotion": "喜悦/悲伤/愤怒/恐惧/爱情/思乡",
                "score": 0.95,
                "keywords": ["明月", "思乡"],
                "description": "这首诗表达了诗人对故乡的思念之情"
            }
        """
        # 基础情感分析
        result = self.analyzer(poetry)[0]

        # 提取关键词
        keywords = self.extract_keywords(poetry)

        # 生成描述
        description = self.generate_description(poetry, result, keywords)

        return {
            "emotion": self.map_emotion(result['label']),
            "score": result['score'],
            "keywords": keywords,
            "description": description
        }

@app.post("/ai/analyze-sentiment")
async def analyze_sentiment(poetry: str):
    """分析诗词情感"""
    analyzer = SentimentAnalyzer()
    result = await analyzer.analyze(poetry)
    return result
```

**应用场景**：
- 诗词详情页展示情感标签
- 按情感筛选诗词
- 情感推荐（根据用户情绪推荐）

---

#### 4. 朝代/作者识别 🏛️

**技术方案**：BERT文本分类

```python
class DynastyClassifier:
    """朝代识别"""

    def __init__(self):
        self.model = pipeline(
            "text-classification",
            model="bert-base-chinese-dynasty"
        )

    async def classify(self, poetry: str) -> dict:
        """
        识别诗词朝代

        Returns:
            {
                "dynasty": "唐代",
                "confidence": 0.92,
                "possible_authors": ["李白", "杜甫", "王维"]
            }
        """
        result = self.model(poetry)[0]
        dynasty = result['label']
        confidence = result['score']

        # 根据朝代和风格推测可能的作者
        possible_authors = await self.predict_authors(poetry, dynasty)

        return {
            "dynasty": dynasty,
            "confidence": confidence,
            "possible_authors": possible_authors
        }
```

**应用场景**：
- 用户上传诗词，自动识别朝代
- 诗词知识问答游戏
- 辅助内容审核

---

#### 5. 语义搜索 🔍

**技术方案**：Sentence-BERT + 向量检索

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SemanticSearch:
    """语义搜索引擎"""

    def __init__(self):
        # 加载模型
        self.model = SentenceTransformer('paraphrase-multilingual-MiniLM-L12-v2')

        # 加载诗词向量索引
        self.index = faiss.read_index("poetry_vectors.index")

        # 诗词ID映射
        self.id_mapping = self.load_id_mapping()

    async def search(self, query: str, limit: int = 10) -> list:
        """
        语义搜索

        Args:
            query: 搜索关键词（如"思念故乡的诗"）

        Returns:
            相关诗词列表
        """
        # 将查询转为向量
        query_vector = self.model.encode([query])[0]

        # 向量检索
        distances, indices = self.index.search(
            np.array([query_vector]),
            limit
        )

        # 获取诗词信息
        poetry_ids = [self.id_mapping[idx] for idx in indices[0]]
        poetries = await self.get_poetries_by_ids(poetry_ids)

        return poetries

@app.get("/search/semantic")
async def semantic_search(query: str, limit: int = 10):
    """语义搜索"""
    search_engine = SemanticSearch()
    results = await search_engine.search(query, limit)
    return results
```

**应用场景**：
- "表达思乡之情的诗" → 自动找到相关诗词
- "描写春天的词" → 语义匹配
- 比关键词搜索更智能

---

#### 6. OCR识别古诗词图片 📷

**技术方案**：PaddleOCR / Tesseract

```python
from paddleocr import PaddleOCR

class PoetryOCR:
    """诗词图片识别"""

    def __init__(self):
        self.ocr = PaddleOCR(use_angle_cls=True, lang='ch')

    async def recognize(self, image_path: str) -> dict:
        """
        识别图片中的诗词

        Returns:
            {
                "text": "床前明月光，疑是地上霜...",
                "lines": ["床前明月光", "疑是地上霜", ...],
                "confidence": 0.95,
                "matched_poetry": {诗词信息}
            }
        """
        # OCR识别
        result = self.ocr.ocr(image_path, cls=True)

        # 提取文本
        lines = []
        for line in result:
            for word_info in line:
                lines.append(word_info[1][0])

        text = "".join(lines)

        # 在数据库中匹配诗词
        matched_poetry = await self.match_poetry(text)

        return {
            "text": text,
            "lines": lines,
            "confidence": self.calculate_confidence(result),
            "matched_poetry": matched_poetry
        }

@app.post("/ai/ocr")
async def recognize_poetry_image(file: UploadFile):
    """识别诗词图片"""
    # 保存上传的图片
    image_path = await save_upload_file(file)

    # OCR识别
    ocr = PoetryOCR()
    result = await ocr.recognize(image_path)

    return result
```

**应用场景**：
- 拍照识诗
- 识别书法作品
- 辅助录入诗词

---

### 3.2 AI功能的系统架构

```
用户请求
    ↓
FastAPI接口
    ↓
任务分发
    ├─→ [轻量任务] 直接处理 (情感分析、分类等)
    └─→ [重量任务] Celery异步处理 (诗词生成、训练等)
            ↓
        AI模型推理
            ├─→ CPU推理 (轻量模型)
            └─→ GPU推理 (大模型，使用TorchServe)
                ↓
            结果缓存 (Redis)
                ↓
            返回结果
```

---

## 四、核心依赖包

### 4.1 后端（FastAPI）

```txt
# requirements.txt

# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6

# 数据库
sqlalchemy==2.0.23
aiomysql==0.2.0
alembic==1.12.1  # 数据库迁移

# Redis
redis==5.0.1
aioredis==2.0.1

# 认证
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-multipart==0.0.6

# 任务队列
celery==5.3.4
redis==5.0.1

# Elasticsearch
elasticsearch==8.11.0

# 微信相关
pycryptodome==3.19.0
requests==2.31.0

# AI/ML核心库
torch==2.1.0
transformers==4.35.0
sentence-transformers==2.2.2
scikit-learn==1.3.2
numpy==1.24.3
pandas==2.1.3

# OCR
paddleocr==2.7.0
paddlepaddle==2.5.1

# 图像处理
Pillow==10.1.0
opencv-python==4.8.1

# 向量检索
faiss-cpu==1.7.4  # 或 faiss-gpu

# 工具库
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
httpx==0.25.1
aiofiles==23.2.1

# 开发工具
pytest==7.4.3
pytest-asyncio==0.21.1
black==23.11.0
flake8==6.1.0
mypy==1.7.1
```

### 4.2 前端

```json
// 前端依赖与之前相同，无需更改
{
  "dependencies": {
    "vue": "^3.3.0",
    "@dcloudio/uni-app": "^3.0.0",
    "pinia": "^2.1.0",
    "axios": "^1.4.0"
  }
}
```

---

## 五、开发环境搭建

### 5.1 Python环境

```bash
# 1. 安装Python 3.11+（推荐使用pyenv）
pyenv install 3.11.6
pyenv global 3.11.6
python --version  # Python 3.11.6

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 3. 升级pip
pip install --upgrade pip

# 4. 安装依赖
pip install -r requirements.txt

# 5. 安装GPU版PyTorch（如果有GPU）
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

### 5.2 数据库

```bash
# MySQL
mysql --version

# Redis
redis-server --version

# Elasticsearch
curl -X GET "localhost:9200"
```

### 5.3 运行项目

```bash
# 启动FastAPI服务
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# 启动Celery Worker
celery -A app.tasks.celery_app worker --loglevel=info

# 启动Celery Beat（定时任务）
celery -A app.tasks.celery_app beat --loglevel=info
```

---

## 六、项目目录结构（Python后端）

```
server/  (Python FastAPI)
├── app/
│   ├── __init__.py
│   │
│   ├── main.py                 # FastAPI应用入口
│   │
│   ├── core/                   # 核心配置
│   │   ├── __init__.py
│   │   ├── config.py           # 配置管理
│   │   ├── security.py         # 安全相关（JWT、密码）
│   │   └── database.py         # 数据库连接
│   │
│   ├── models/                 # 数据模型（SQLAlchemy）
│   │   ├── __init__.py
│   │   ├── user.py             # 用户模型
│   │   ├── poetry.py           # 诗词模型
│   │   ├── comment.py          # 评论模型
│   │   ├── post.py             # 广场模型
│   │   ├── game.py             # 游戏模型
│   │   └── message.py          # 消息模型
│   │
│   ├── schemas/                # Pydantic模型（API数据验证）
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── poetry.py
│   │   ├── comment.py
│   │   └── ...
│   │
│   ├── api/                    # API路由
│   │   ├── __init__.py
│   │   ├── deps.py             # 依赖注入
│   │   └── v1/                 # API版本1
│   │       ├── __init__.py
│   │       ├── auth.py         # 认证接口
│   │       ├── users.py        # 用户接口
│   │       ├── poetry.py       # 诗词接口
│   │       ├── comments.py     # 评论接口
│   │       ├── square.py       # 广场接口
│   │       ├── game.py         # 游戏接口
│   │       ├── ai.py           # AI接口 🤖
│   │       └── admin.py        # 管理接口
│   │
│   ├── services/               # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   ├── poetry_service.py
│   │   ├── comment_service.py
│   │   ├── search_service.py   # Elasticsearch搜索
│   │   └── ai_service.py       # AI服务 🤖
│   │
│   ├── ai/                     # AI模块 🤖
│   │   ├── __init__.py
│   │   ├── recommender.py      # 推荐引擎
│   │   ├── generator.py        # 诗词生成
│   │   ├── sentiment.py        # 情感分析
│   │   ├── classifier.py       # 分类模型
│   │   ├── semantic_search.py  # 语义搜索
│   │   ├── ocr.py              # OCR识别
│   │   └── models/             # 模型文件目录
│   │       ├── gpt2-poetry/
│   │       ├── bert-classifier/
│   │       └── ...
│   │
│   ├── tasks/                  # Celery异步任务
│   │   ├── __init__.py
│   │   ├── celery_app.py       # Celery配置
│   │   ├── ai_tasks.py         # AI异步任务
│   │   ├── email_tasks.py      # 邮件任务
│   │   └── schedule_tasks.py   # 定时任务
│   │
│   ├── websocket/              # WebSocket
│   │   ├── __init__.py
│   │   ├── manager.py          # 连接管理
│   │   └── game_handler.py     # 游戏处理
│   │
│   ├── utils/                  # 工具函数
│   │   ├── __init__.py
│   │   ├── wechat.py           # 微信API
│   │   ├── redis_client.py     # Redis客户端
│   │   ├── oss.py              # 对象存储
│   │   └── helpers.py          # 辅助函数
│   │
│   └── middleware/             # 中间件
│       ├── __init__.py
│       ├── cors.py             # CORS
│       ├── rate_limit.py       # 限流
│       └── logging.py          # 日志
│
├── alembic/                    # 数据库迁移
│   ├── versions/
│   └── env.py
│
├── tests/                      # 测试
│   ├── test_api/
│   ├── test_services/
│   └── test_ai/
│
├── scripts/                    # 脚本
│   ├── import_poetry.py        # 导入诗词数据
│   ├── train_model.py          # 训练AI模型
│   └── init_db.py              # 初始化数据库
│
├── requirements.txt            # 依赖包
├── requirements-dev.txt        # 开发依赖
├── .env                        # 环境变量
├── .env.example
├── alembic.ini                 # Alembic配置
├── pytest.ini                  # Pytest配置
├── Dockerfile
├── docker-compose.yml
└── README.md
```

---

## 七、开发工具推荐

### 7.1 IDE

| 工具 | 推荐用途 | 推荐指数 |
|------|---------|---------|
| **PyCharm Professional** | Python开发首选，功能最强 | ⭐⭐⭐⭐⭐ |
| **VS Code + Python插件** | 轻量级，免费 | ⭐⭐⭐⭐⭐ |
| **Jupyter Notebook** | AI模型实验、数据分析 | ⭐⭐⭐⭐⭐ |

**VS Code推荐插件**：
```
- Python (Microsoft)
- Pylance (类型检查)
- Black Formatter (代码格式化)
- Ruff (代码检查)
- autoDocstring (自动生成文档字符串)
- GitLens
- Thunder Client (API测试)
```

---

### 7.2 AI/ML开发工具

| 工具 | 用途 | 推荐指数 |
|------|------|---------|
| **Jupyter Lab** | 模型实验、数据分析 | ⭐⭐⭐⭐⭐ |
| **TensorBoard** | 模型训练可视化 | ⭐⭐⭐⭐⭐ |
| **Weights & Biases** | 实验管理、模型对比 | ⭐⭐⭐⭐⭐ |
| **HuggingFace Hub** | 预训练模型下载 | ⭐⭐⭐⭐⭐ |

---

## 八、AI模型资源

### 8.1 推荐的预训练模型

#### 诗词生成
- **GPT2-Chinese-Poetry**: https://huggingface.co/uer/gpt2-chinese-poetry
- **ChatGLM-6B**: https://huggingface.co/THUDM/chatglm-6b
- **通义千问**: https://github.com/QwenLM/Qwen

#### 文本分类/情感分析
- **Chinese-RoBERTa**: https://huggingface.co/hfl/chinese-roberta-wwm-ext
- **BERT-Base-Chinese**: https://huggingface.co/bert-base-chinese

#### 语义搜索
- **Sentence-BERT中文**: https://huggingface.co/shibing624/text2vec-base-chinese

#### OCR
- **PaddleOCR**: https://github.com/PaddlePaddle/PaddleOCR

### 8.2 训练数据集

- **Chinese-Poetry数据集**: https://github.com/chinese-poetry/chinese-poetry
  - 5.5万首唐诗
  - 26万首宋诗
  - 2.1万首宋词

---

## 九、部署方案

### 9.1 Docker部署

```yaml
# docker-compose.yml
version: '3.8'

services:
  # FastAPI应用
  api:
    build: ./server
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=mysql+aiomysql://user:pass@mysql:3306/poetry_db
      - REDIS_URL=redis://redis:6379/0
    depends_on:
      - mysql
      - redis
    volumes:
      - ./server:/app
      - ai_models:/app/models  # AI模型持久化
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]  # GPU支持

  # Celery Worker
  celery_worker:
    build: ./server
    command: celery -A app.tasks.celery_app worker --loglevel=info
    depends_on:
      - redis
      - mysql
    volumes:
      - ./server:/app
      - ai_models:/app/models

  # Celery Beat
  celery_beat:
    build: ./server
    command: celery -A app.tasks.celery_app beat --loglevel=info
    depends_on:
      - redis

  # MySQL
  mysql:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: password
      MYSQL_DATABASE: poetry_db
    volumes:
      - mysql_data:/var/lib/mysql
    ports:
      - "3306:3306"

  # Redis
  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

  # Elasticsearch
  elasticsearch:
    image: elasticsearch:8.11.0
    environment:
      - discovery.type=single-node
      - xpack.security.enabled=false
    ports:
      - "9200:9200"
    volumes:
      - es_data:/usr/share/elasticsearch/data

  # Nginx
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx/nginx.conf:/etc/nginx/nginx.conf
      - ./nginx/ssl:/etc/nginx/ssl
    depends_on:
      - api

volumes:
  mysql_data:
  redis_data:
  es_data:
  ai_models:  # AI模型存储
```

### 9.2 GPU服务器配置建议

**AI模型推理服务器**：
- CPU: 8核+
- 内存: 32GB+
- GPU: NVIDIA RTX 3060 (12GB) 或更高
- 存储: 500GB+ SSD
- 系统: Ubuntu 22.04 LTS

**无GPU方案**：
- 使用CPU推理（速度较慢）
- 使用云服务商的AI推理服务：
  - 阿里云PAI
  - 腾讯云TI-EMS
  - AWS SageMaker

---

## 十、成本估算（含AI）

### 10.1 服务器成本（月）

| 项目 | 配置 | 价格 |
|------|------|------|
| **Web服务器** | 2核4G | 100-200元 |
| **AI推理服务器** | 8核32G + GPU | 1000-2000元 |
| **MySQL** | 1核2G | 50-100元 |
| **Redis** | 256MB | 30-50元 |
| **OSS存储** | 20GB + 流量 | 20-50元 |
| **GPU云服务器（可选）** | NVIDIA T4 | 3-5元/小时 |

**总计**：约 **1200-2400元/月**（含GPU）
**无GPU方案**：约 **200-400元/月**

### 10.2 AI服务成本优化

1. **模型压缩**：使用量化、剪枝减小模型大小
2. **模型缓存**：使用Redis缓存常见结果
3. **按需启动**：低峰期停止GPU服务器
4. **批量推理**：合并多个请求批量处理
5. **使用小模型**：优先使用轻量级模型

---

## 十一、总结与建议

### ✅ 最终技术栈

```
🎯 前端
├─ uni-app (Vue 3 + TypeScript)
└─ Vue 3 + Element Plus

🎯 后端 (Python 3.11+)
├─ FastAPI (高性能异步框架)
├─ SQLAlchemy 2.0 (异步ORM)
├─ Celery (任务队列)
└─ WebSocket (实时通信)

🎯 数据层
├─ MySQL 8.0 (主数据库)
├─ Redis 6+ (缓存)
└─ Elasticsearch (搜索)

🤖 AI/ML层
├─ PyTorch (深度学习框架)
├─ Transformers (预训练模型)
├─ Sentence-BERT (语义搜索)
└─ PaddleOCR (OCR识别)
```

### 📊 选择Python的核心优势

1. **AI生态最强**：PyTorch、TensorFlow、HuggingFace等
2. **开发效率高**：代码简洁，易于维护
3. **模型丰富**：海量预训练模型可直接使用
4. **社区活跃**：AI/ML问题容易解决
5. **扩展性强**：从原型到生产无缝过渡

### 🚀 MVP开发优先级

**第一阶段（4-6周）**：
1. 基础功能（用户、诗词、搜索）
2. 简单推荐（基于热度）

**第二阶段（3-4周）**：
3. 社交功能（评论、点赞、关注）
4. 智能推荐（AI）

**第三阶段（4-5周）**：
5. AI生成诗词
6. 情感分析
7. 飞花令游戏

### 💡 AI集成建议

1. **逐步引入**：先用简单算法，再上AI
2. **离线训练**：模型训练在本地/云端进行
3. **在线推理**：部署轻量模型实时预测
4. **监控评估**：持续监控AI效果，定期优化

---

**Python + FastAPI + AI = 诗词平台的最佳选择！** 🎉🤖
