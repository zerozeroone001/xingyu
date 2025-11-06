# 诗词程序 - AI模型集成方案

## 一、AI功能总览

### 1.1 核心AI能力

| 功能 | 技术方案 | 优先级 | 开发周期 | GPU需求 |
|------|---------|--------|---------|---------|
| **智能推荐** | 协同过滤 + 内容推荐 + 深度学习 | ⭐⭐⭐⭐⭐ | 2-3周 | 可选 |
| **AI诗词生成** | GPT-2中文 / ChatGLM | ⭐⭐⭐⭐ | 2-3周 | 推荐 |
| **情感分析** | RoBERTa情感模型 | ⭐⭐⭐⭐ | 1周 | 可选 |
| **朝代/作者识别** | BERT文本分类 | ⭐⭐⭐ | 1-2周 | 可选 |
| **语义搜索** | Sentence-BERT + Faiss | ⭐⭐⭐⭐⭐ | 1-2周 | 可选 |
| **OCR识别** | PaddleOCR | ⭐⭐⭐ | 1周 | 可选 |
| **智能问答** | RAG (检索增强生成) | ⭐⭐⭐ | 2-3周 | 推荐 |
| **诗词纠错** | BERT + 规则引擎 | ⭐⭐ | 1-2周 | 可选 |

---

## 二、详细功能设计

### 2.1 智能推荐系统 🎯

#### 功能描述
基于用户行为、诗词特征、社交关系等多维度数据，为用户智能推荐感兴趣的诗词。

#### 技术架构

```
用户行为数据
    ↓
特征工程
    ├─→ 用户特征（年龄、地域、兴趣）
    ├─→ 诗词特征（朝代、类型、主题、情感）
    ├─→ 交互特征（点赞、收藏、浏览时长）
    └─→ 上下文特征（时间、节日、天气）
        ↓
推荐算法
    ├─→ [召回层] 协同过滤 (快速筛选候选)
    ├─→ [召回层] 内容推荐 (基于相似度)
    ├─→ [排序层] 深度学习模型 (精准排序)
    └─→ [重排层] 规则引擎 (多样性、新颖性)
        ↓
推荐结果
```

#### 实现方案

##### 方案一：协同过滤（初期推荐，不需要GPU）

```python
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import pandas as pd

class CollaborativeFiltering:
    """协同过滤推荐"""

    def __init__(self, db_session):
        self.db = db_session
        self.user_item_matrix = None  # 用户-诗词交互矩阵
        self.similarity_matrix = None  # 相似度矩阵

    async def build_matrix(self):
        """构建用户-诗词交互矩阵"""
        # 获取所有用户交互数据（点赞、收藏、浏览）
        interactions = await self.db.execute(
            """
            SELECT user_id, poetry_id,
                   SUM(CASE WHEN action='like' THEN 3
                            WHEN action='collect' THEN 5
                            WHEN action='read' THEN 1
                            ELSE 0 END) as score
            FROM user_interactions
            GROUP BY user_id, poetry_id
            """
        )

        # 构建矩阵
        df = pd.DataFrame(interactions)
        self.user_item_matrix = df.pivot(
            index='user_id',
            columns='poetry_id',
            values='score'
        ).fillna(0)

        # 计算用户相似度（基于用户）
        self.similarity_matrix = cosine_similarity(self.user_item_matrix)

    async def recommend(self, user_id: int, top_k: int = 10):
        """
        为用户推荐诗词

        Args:
            user_id: 用户ID
            top_k: 推荐数量

        Returns:
            推荐的诗词ID列表
        """
        if user_id not in self.user_item_matrix.index:
            # 新用户：推荐热门诗词
            return await self.get_popular_poetries(top_k)

        # 找到相似用户
        user_idx = self.user_item_matrix.index.get_loc(user_id)
        similar_users = self.similarity_matrix[user_idx].argsort()[-10:][::-1]

        # 聚合相似用户喜欢的诗词
        recommendations = []
        user_interacted = set(
            self.user_item_matrix.iloc[user_idx][
                self.user_item_matrix.iloc[user_idx] > 0
            ].index
        )

        for sim_user_idx in similar_users:
            if sim_user_idx == user_idx:
                continue

            sim_user_items = self.user_item_matrix.iloc[sim_user_idx]
            for poetry_id, score in sim_user_items[sim_user_items > 0].items():
                if poetry_id not in user_interacted:
                    recommendations.append({
                        'poetry_id': poetry_id,
                        'score': score * self.similarity_matrix[user_idx][sim_user_idx]
                    })

        # 按分数排序
        recommendations = sorted(
            recommendations,
            key=lambda x: x['score'],
            reverse=True
        )[:top_k]

        return [r['poetry_id'] for r in recommendations]

    async def get_popular_poetries(self, top_k: int):
        """获取热门诗词（冷启动）"""
        result = await self.db.execute(
            """
            SELECT id FROM poetry
            ORDER BY (like_count * 3 + collect_count * 5 + read_count) DESC
            LIMIT :limit
            """,
            {"limit": top_k}
        )
        return [row[0] for row in result]
```

##### 方案二：深度学习推荐（后期优化，建议使用GPU）

```python
import torch
import torch.nn as nn

class DeepRecommender(nn.Module):
    """深度学习推荐模型（Wide & Deep架构）"""

    def __init__(self, n_users, n_poetries, embedding_dim=64):
        super().__init__()

        # Wide部分：线性模型（记忆能力）
        self.wide = nn.Linear(n_users + n_poetries, 1)

        # Deep部分：深度神经网络（泛化能力）
        self.user_embedding = nn.Embedding(n_users, embedding_dim)
        self.poetry_embedding = nn.Embedding(n_poetries, embedding_dim)

        self.deep = nn.Sequential(
            nn.Linear(embedding_dim * 2, 128),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(64, 1)
        )

    def forward(self, user_ids, poetry_ids, user_features, poetry_features):
        # Wide部分
        wide_input = torch.cat([user_features, poetry_features], dim=1)
        wide_out = self.wide(wide_input)

        # Deep部分
        user_emb = self.user_embedding(user_ids)
        poetry_emb = self.poetry_embedding(poetry_ids)
        deep_input = torch.cat([user_emb, poetry_emb], dim=1)
        deep_out = self.deep(deep_input)

        # 组合
        output = torch.sigmoid(wide_out + deep_out)
        return output


class RecommendationService:
    """推荐服务"""

    def __init__(self):
        self.model = DeepRecommender(
            n_users=100000,
            n_poetries=50000,
            embedding_dim=64
        )
        self.model.load_state_dict(torch.load('models/recommender.pth'))
        self.model.eval()

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model.to(self.device)

    async def predict(self, user_id: int, poetry_ids: list):
        """
        预测用户对诗词的兴趣分数

        Returns:
            {poetry_id: score} 字典
        """
        # 准备输入数据
        user_ids = torch.tensor([user_id] * len(poetry_ids)).to(self.device)
        poetry_ids_tensor = torch.tensor(poetry_ids).to(self.device)

        # 获取特征
        user_features = await self.get_user_features(user_id)
        poetry_features = await self.get_poetry_features(poetry_ids)

        # 预测
        with torch.no_grad():
            scores = self.model(
                user_ids,
                poetry_ids_tensor,
                user_features,
                poetry_features
            )

        # 返回结果
        results = {
            pid: score.item()
            for pid, score in zip(poetry_ids, scores)
        }
        return results

    async def recommend(self, user_id: int, top_k: int = 10):
        """推荐诗词"""
        # 1. 召回候选（快速筛选1000个候选）
        candidates = await self.recall_candidates(user_id, n=1000)

        # 2. 精准排序（深度模型）
        scores = await self.predict(user_id, candidates)

        # 3. 重排序（多样性、新颖性）
        final_recommendations = await self.rerank(
            user_id,
            scores,
            top_k
        )

        return final_recommendations
```

#### 数据存储

```python
# Redis缓存推荐结果
class RecommendationCache:
    """推荐结果缓存"""

    def __init__(self, redis_client):
        self.redis = redis_client

    async def get(self, user_id: int):
        """获取缓存的推荐"""
        key = f"recommend:user:{user_id}"
        result = await self.redis.get(key)
        if result:
            return json.loads(result)
        return None

    async def set(self, user_id: int, recommendations: list, ttl: int = 3600):
        """缓存推荐结果（1小时）"""
        key = f"recommend:user:{user_id}"
        await self.redis.setex(
            key,
            ttl,
            json.dumps(recommendations)
        )
```

---

### 2.2 AI诗词生成 ✍️

#### 功能描述
用户输入主题、风格、朝代等条件，AI自动生成诗词。

#### 应用场景
1. **创作辅助**：用户输入主题，AI生成诗词初稿
2. **飞花令AI对手**：与AI对战飞花令
3. **诗词续写**：给出前几句，AI续写
4. **风格仿写**：仿写特定诗人的风格

#### 技术方案对比

| 方案 | 模型 | 效果 | 速度 | GPU需求 | 推荐 |
|------|------|------|------|---------|------|
| **轻量方案** | GPT-2-Small (117M) | ⭐⭐⭐ | 快 | CPU可 | 初期 |
| **平衡方案** | GPT-2-Medium (345M) | ⭐⭐⭐⭐ | 中等 | 推荐GPU | ⭐ |
| **高质量方案** | ChatGLM-6B | ⭐⭐⭐⭐⭐ | 慢 | 必须GPU | 后期 |

#### 实现代码

```python
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
import torch

class PoetryGenerator:
    """诗词生成器"""

    def __init__(self, model_name="uer/gpt2-chinese-poetry"):
        """
        初始化生成器

        Args:
            model_name: 模型名称，可选：
                - "uer/gpt2-chinese-poetry" (轻量，CPU可用)
                - "THUDM/chatglm-6b" (高质量，需要GPU)
        """
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            torch_dtype=torch.float16,  # 使用半精度节省显存
            device_map="auto"  # 自动分配到GPU/CPU
        )
        self.model.eval()

        # 生成配置
        self.generation_config = GenerationConfig(
            max_length=100,
            num_return_sequences=1,
            no_repeat_ngram_size=2,  # 避免重复
            top_k=50,
            top_p=0.95,
            temperature=0.8,
            do_sample=True,
            pad_token_id=self.tokenizer.pad_token_id,
            eos_token_id=self.tokenizer.eos_token_id
        )

    async def generate(
        self,
        prompt: str,
        style: str = "五言绝句",
        dynasty: str = "唐代",
        num_return: int = 3
    ) -> list[str]:
        """
        生成诗词

        Args:
            prompt: 主题或首句，如"明月"、"春天"
            style: 诗词风格，如"五言绝句"、"七言律诗"、"词"
            dynasty: 朝代风格，如"唐代"、"宋代"
            num_return: 返回数量

        Returns:
            生成的诗词列表
        """
        # 构造提示词
        input_text = self._build_prompt(prompt, style, dynasty)

        # Tokenize
        inputs = self.tokenizer(
            input_text,
            return_tensors="pt",
            padding=True
        ).to(self.model.device)

        # 生成
        with torch.no_grad():
            outputs = self.model.generate(
                **inputs,
                generation_config=self.generation_config,
                num_return_sequences=num_return
            )

        # 解码
        generated_texts = [
            self.tokenizer.decode(output, skip_special_tokens=True)
            for output in outputs
        ]

        # 后处理
        poetries = [
            self._post_process(text, style)
            for text in generated_texts
        ]

        return poetries

    def _build_prompt(self, prompt: str, style: str, dynasty: str) -> str:
        """构造提示词"""
        templates = {
            "五言绝句": f"[{dynasty}][五言绝句]{prompt}",
            "七言绝句": f"[{dynasty}][七言绝句]{prompt}",
            "五言律诗": f"[{dynasty}][五言律诗]{prompt}",
            "七言律诗": f"[{dynasty}][七言律诗]{prompt}",
            "词": f"[{dynasty}][词]{prompt}",
        }
        return templates.get(style, f"[{dynasty}]{prompt}")

    def _post_process(self, text: str, style: str) -> str:
        """后处理生成的诗词"""
        # 移除提示词标记
        text = re.sub(r'\[.*?\]', '', text)

        # 根据风格格式化
        if "五言绝句" in style:
            # 四句，每句5字
            lines = self._split_by_punctuation(text)[:4]
            lines = [line[:5] for line in lines]
        elif "七言绝句" in style:
            # 四句，每句7字
            lines = self._split_by_punctuation(text)[:4]
            lines = [line[:7] for line in lines]
        elif "五言律诗" in style:
            # 八句，每句5字
            lines = self._split_by_punctuation(text)[:8]
            lines = [line[:5] for line in lines]
        elif "七言律诗" in style:
            # 八句，每句7字
            lines = self._split_by_punctuation(text)[:8]
            lines = [line[:7] for line in lines]
        else:
            lines = self._split_by_punctuation(text)

        # 添加标点
        formatted = "，\n".join(lines[:-1]) + "。"
        if len(lines) > 1:
            mid = len(lines) // 2
            formatted = "，\n".join(lines[:mid-1]) + "。\n" + \
                       "，\n".join(lines[mid:]) + "。"

        return formatted.strip()

    def _split_by_punctuation(self, text: str) -> list[str]:
        """按标点符号分句"""
        text = re.sub(r'[，。！？；：、]', '\n', text)
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        return lines


# FastAPI接口
@app.post("/ai/generate-poetry")
async def generate_poetry(request: PoetryGenerateRequest):
    """
    AI生成诗词

    Request:
        {
            "prompt": "明月",
            "style": "五言绝句",
            "dynasty": "唐代",
            "num_return": 3
        }

    Response:
        {
            "poetries": [
                "明月照高楼，\n流光正徘徊。\n上有愁思妇，\n悲叹有余哀。",
                "明月皎夜光，\n促织鸣东壁。\n玉衡指孟冬，\n众星何历历。",
                ...
            ],
            "prompt": "明月",
            "style": "五言绝句"
        }
    """
    generator = PoetryGenerator()

    poetries = await generator.generate(
        prompt=request.prompt,
        style=request.style,
        dynasty=request.dynasty,
        num_return=request.num_return
    )

    return {
        "poetries": poetries,
        "prompt": request.prompt,
        "style": request.style,
        "dynasty": request.dynasty
    }
```

#### 异步生成（Celery）

对于大模型（如ChatGLM-6B），推理时间较长，应使用异步任务：

```python
from celery import Celery

celery_app = Celery('poetry', broker='redis://localhost:6379/0')

@celery_app.task
def generate_poetry_async(prompt: str, style: str, dynasty: str):
    """异步生成诗词"""
    generator = PoetryGenerator(model_name="THUDM/chatglm-6b")
    poetries = generator.generate(prompt, style, dynasty)
    return poetries

# API接口
@app.post("/ai/generate-poetry-async")
async def generate_poetry_async_api(request: PoetryGenerateRequest):
    """异步生成诗词（返回任务ID）"""
    task = generate_poetry_async.delay(
        request.prompt,
        request.style,
        request.dynasty
    )

    return {
        "task_id": task.id,
        "status": "pending",
        "message": "诗词生成中，请稍后查询结果"
    }

@app.get("/ai/task/{task_id}")
async def get_task_result(task_id: str):
    """查询异步任务结果"""
    task = celery_app.AsyncResult(task_id)

    if task.ready():
        return {
            "task_id": task_id,
            "status": "completed",
            "result": task.result
        }
    else:
        return {
            "task_id": task_id,
            "status": "pending",
            "message": "诗词生成中..."
        }
```

---

### 2.3 情感分析 😊😢

#### 功能描述
分析诗词表达的情感（喜悦、悲伤、思乡、爱情等）。

#### 应用场景
- 诗词详情页展示情感标签
- 按情感筛选诗词
- 情感推荐（根据用户情绪推荐）

#### 实现代码

```python
from transformers import pipeline
import torch

class SentimentAnalyzer:
    """诗词情感分析"""

    def __init__(self):
        # 加载情感分析模型
        self.analyzer = pipeline(
            "text-classification",
            model="uer/roberta-base-finetuned-chinanews-chinese",
            device=0 if torch.cuda.is_available() else -1
        )

        # 情感映射
        self.emotion_map = {
            'LABEL_0': '喜悦',
            'LABEL_1': '悲伤',
            'LABEL_2': '愤怒',
            'LABEL_3': '恐惧',
            'LABEL_4': '惊讶',
            'LABEL_5': '厌恶'
        }

        # 诗词特定情感关键词
        self.poetry_emotions = {
            '思乡': ['故乡', '家乡', '思归', '乡愁', '游子'],
            '爱情': ['相思', '离别', '思君', '情郎', '佳人'],
            '豪放': ['壮志', '豪情', '气吞', '万里', '长风'],
            '婉约': ['细雨', '轻风', '幽怨', '凄美', '柔情'],
            '田园': ['田园', '山水', '桃花', '农家', '耕种'],
            '边塞': ['边关', '戍边', '沙场', '征战', '烽火']
        }

    async def analyze(self, poetry_content: str) -> dict:
        """
        分析诗词情感

        Returns:
            {
                "primary_emotion": "悲伤",
                "secondary_emotions": ["思乡", "离别"],
                "score": 0.95,
                "keywords": ["明月", "故乡", "思归"],
                "description": "这首诗表达了诗人对故乡的深切思念"
            }
        """
        # 1. 基础情感分析
        result = self.analyzer(poetry_content[:512])[0]  # 限制长度
        primary_emotion = self.emotion_map.get(result['label'], '未知')
        score = result['score']

        # 2. 提取诗词特定情感
        secondary_emotions = self._extract_poetry_emotions(poetry_content)

        # 3. 提取关键词
        keywords = self._extract_keywords(poetry_content)

        # 4. 生成情感描述
        description = self._generate_description(
            primary_emotion,
            secondary_emotions,
            keywords
        )

        return {
            "primary_emotion": primary_emotion,
            "secondary_emotions": secondary_emotions,
            "score": score,
            "keywords": keywords,
            "description": description
        }

    def _extract_poetry_emotions(self, text: str) -> list[str]:
        """提取诗词特定情感"""
        emotions = []
        for emotion, keywords in self.poetry_emotions.items():
            if any(keyword in text for keyword in keywords):
                emotions.append(emotion)
        return emotions[:3]  # 最多3个

    def _extract_keywords(self, text: str) -> list[str]:
        """提取关键词（简化版，可用jieba优化）"""
        # TODO: 使用jieba分词 + TF-IDF提取关键词
        import jieba.analyse
        keywords = jieba.analyse.extract_tags(text, topK=5)
        return keywords

    def _generate_description(
        self,
        primary_emotion: str,
        secondary_emotions: list[str],
        keywords: list[str]
    ) -> str:
        """生成情感描述"""
        templates = {
            '喜悦': f"这首诗洋溢着{primary_emotion}之情",
            '悲伤': f"这首诗流露出深深的{primary_emotion}",
            '思乡': f"这首诗表达了对故乡的思念",
            '爱情': f"这首诗描绘了动人的爱情",
        }

        base = templates.get(
            primary_emotion,
            f"这首诗的主要情感是{primary_emotion}"
        )

        if secondary_emotions:
            base += f"，并蕴含{、'.join(secondary_emotions)}之意"

        if keywords:
            base += f"，通过{keywords[0]}等意象表现"

        return base + "。"


# API接口
@app.post("/ai/analyze-sentiment")
async def analyze_sentiment(poetry_id: int):
    """分析诗词情感"""
    # 获取诗词内容
    poetry = await db.get(Poetry, poetry_id)
    if not poetry:
        raise HTTPException(404, "诗词不存在")

    # 分析情感
    analyzer = SentimentAnalyzer()
    result = await analyzer.analyze(poetry.content)

    # 保存到数据库
    await db.execute(
        """
        UPDATE poetry
        SET emotion_primary = :primary,
            emotion_secondary = :secondary,
            emotion_keywords = :keywords
        WHERE id = :id
        """,
        {
            "primary": result['primary_emotion'],
            "secondary": json.dumps(result['secondary_emotions']),
            "keywords": json.dumps(result['keywords']),
            "id": poetry_id
        }
    )

    return result
```

---

### 2.4 语义搜索 🔍

#### 功能描述
用户输入"描写春天的诗"，系统通过语义理解找到相关诗词，而不是简单的关键词匹配。

#### 技术方案

```python
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class SemanticSearchEngine:
    """语义搜索引擎"""

    def __init__(self):
        # 加载Sentence-BERT模型
        self.model = SentenceTransformer(
            'shibing624/text2vec-base-chinese'
        )

        # 加载Faiss向量索引
        self.index = faiss.read_index("data/poetry_vectors.index")

        # 加载诗词ID映射
        self.id_mapping = np.load("data/poetry_id_mapping.npy")

        # 维度
        self.dimension = 768

    async def build_index(self, poetries: list):
        """
        构建向量索引（离线任务）

        Args:
            poetries: [{'id': 1, 'title': '', 'content': ''}, ...]
        """
        # 提取文本
        texts = [
            f"{p['title']} {p['content']}"
            for p in poetries
        ]

        # 批量编码
        vectors = self.model.encode(
            texts,
            batch_size=32,
            show_progress_bar=True
        )

        # 归一化（用于余弦相似度）
        vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)

        # 创建Faiss索引（使用内积，相当于余弦相似度）
        index = faiss.IndexFlatIP(self.dimension)
        index.add(vectors.astype('float32'))

        # 保存
        faiss.write_index(index, "data/poetry_vectors.index")

        # 保存ID映射
        id_mapping = np.array([p['id'] for p in poetries])
        np.save("data/poetry_id_mapping.npy", id_mapping)

        print(f"索引构建完成，共 {len(poetries)} 首诗词")

    async def search(
        self,
        query: str,
        top_k: int = 10,
        filters: dict = None
    ) -> list:
        """
        语义搜索

        Args:
            query: 查询语句，如"描写春天的诗"
            top_k: 返回数量
            filters: 过滤条件，如 {"dynasty": "唐代"}

        Returns:
            [
                {
                    'poetry_id': 123,
                    'score': 0.95,
                    'title': '春晓',
                    'content': '...'
                },
                ...
            ]
        """
        # 1. 将查询转为向量
        query_vector = self.model.encode([query])[0]
        query_vector = query_vector / np.linalg.norm(query_vector)  # 归一化

        # 2. 向量检索
        scores, indices = self.index.search(
            np.array([query_vector], dtype='float32'),
            top_k * 3  # 多取一些，用于后续过滤
        )

        # 3. 获取诗词ID
        poetry_ids = self.id_mapping[indices[0]].tolist()

        # 4. 从数据库获取诗词详情
        poetries = await db.execute(
            """
            SELECT id, title, content, author, dynasty
            FROM poetry
            WHERE id IN :ids
            """,
            {"ids": tuple(poetry_ids)}
        )

        # 5. 应用过滤条件
        if filters:
            poetries = [
                p for p in poetries
                if all(
                    getattr(p, key) == value
                    for key, value in filters.items()
                )
            ]

        # 6. 添加相似度分数
        poetry_score_map = {
            pid: score
            for pid, score in zip(poetry_ids, scores[0])
        }

        results = [
            {
                'poetry_id': p.id,
                'title': p.title,
                'content': p.content,
                'author': p.author,
                'dynasty': p.dynasty,
                'score': float(poetry_score_map.get(p.id, 0))
            }
            for p in poetries[:top_k]
        ]

        return results


# API接口
@app.get("/search/semantic")
async def semantic_search(
    query: str,
    top_k: int = 10,
    dynasty: str = None,
    poet: str = None
):
    """
    语义搜索

    Examples:
        /search/semantic?query=描写春天的诗
        /search/semantic?query=思念故乡&dynasty=唐代
    """
    search_engine = SemanticSearchEngine()

    # 构建过滤条件
    filters = {}
    if dynasty:
        filters['dynasty'] = dynasty
    if poet:
        filters['author'] = poet

    # 搜索
    results = await search_engine.search(query, top_k, filters)

    return {
        "query": query,
        "results": results,
        "total": len(results)
    }


# 后台任务：定期重建索引
@celery_app.task
def rebuild_search_index():
    """重建搜索索引（每周执行一次）"""
    # 获取所有诗词
    poetries = db.query(Poetry).all()

    # 构建索引
    engine = SemanticSearchEngine()
    asyncio.run(engine.build_index(poetries))
```

---

### 2.5 OCR识别 📷

#### 功能描述
用户拍摄古诗词图片，系统自动识别文字并匹配诗词。

#### 实现代码

```python
from paddleocr import PaddleOCR
from PIL import Image
import difflib

class PoetryOCR:
    """诗词OCR识别"""

    def __init__(self):
        # 初始化PaddleOCR
        self.ocr = PaddleOCR(
            use_angle_cls=True,  # 文本方向分类
            lang='ch',           # 中文
            use_gpu=torch.cuda.is_available()
        )

    async def recognize(self, image_path: str) -> dict:
        """
        识别图片中的诗词

        Returns:
            {
                "text": "床前明月光，疑是地上霜。举头望明月，低头思故乡。",
                "lines": ["床前明月光", "疑是地上霜", ...],
                "confidence": 0.96,
                "matched_poetry": {
                    "id": 123,
                    "title": "静夜思",
                    "author": "李白",
                    "similarity": 0.98
                }
            }
        """
        # 1. OCR识别
        result = self.ocr.ocr(image_path, cls=True)

        # 2. 提取文本和置信度
        lines = []
        confidences = []

        for line in result:
            for word_info in line:
                text = word_info[1][0]  # 文本
                conf = word_info[1][1]  # 置信度
                lines.append(text)
                confidences.append(conf)

        # 合并文本
        full_text = "".join(lines)
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0

        # 3. 清洗文本（去除标点、空格）
        cleaned_text = re.sub(r'[^\u4e00-\u9fa5]', '', full_text)

        # 4. 在数据库中匹配诗词
        matched_poetry = await self._match_poetry(cleaned_text)

        return {
            "text": full_text,
            "lines": lines,
            "confidence": float(avg_confidence),
            "matched_poetry": matched_poetry
        }

    async def _match_poetry(self, text: str) -> dict:
        """
        在数据库中匹配诗词

        使用编辑距离算法找到最相似的诗词
        """
        # 查询所有诗词（优化：可以用Elasticsearch预筛选）
        poetries = await db.execute(
            """
            SELECT id, title, content, author
            FROM poetry
            WHERE LENGTH(content) BETWEEN :min AND :max
            """,
            {
                "min": len(text) - 20,
                "max": len(text) + 20
            }
        )

        # 计算相似度
        best_match = None
        best_similarity = 0

        for poetry in poetries:
            # 清洗诗词内容
            poetry_text = re.sub(r'[^\u4e00-\u9fa5]', '', poetry.content)

            # 计算相似度（使用difflib）
            similarity = difflib.SequenceMatcher(
                None,
                text,
                poetry_text
            ).ratio()

            if similarity > best_similarity:
                best_similarity = similarity
                best_match = poetry

        if best_match and best_similarity > 0.7:  # 阈值70%
            return {
                "id": best_match.id,
                "title": best_match.title,
                "content": best_match.content,
                "author": best_match.author,
                "similarity": float(best_similarity)
            }

        return None


# API接口
@app.post("/ai/ocr")
async def recognize_poetry_image(file: UploadFile):
    """
    识别诗词图片

    Request:
        multipart/form-data
        file: 图片文件

    Response:
        {
            "text": "床前明月光...",
            "matched_poetry": {...}
        }
    """
    # 保存上传的图片
    file_path = f"/tmp/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())

    # OCR识别
    ocr = PoetryOCR()
    result = await ocr.recognize(file_path)

    # 删除临时文件
    os.remove(file_path)

    return result
```

---

## 三、AI模型部署方案

### 3.1 部署架构

```
┌─────────────────────────────────────────┐
│         FastAPI主服务（8000端口）          │
│  - 业务逻辑                              │
│  - 轻量AI模型（情感分析、分类等）          │
└─────────────────────────────────────────┘
            ↓ HTTP/gRPC
┌─────────────────────────────────────────┐
│      AI模型推理服务（GPU服务器）           │
│  - 诗词生成（ChatGLM-6B）                │
│  - 大模型推理                            │
│  使用 TorchServe / BentoML              │
└─────────────────────────────────────────┘
            ↓ 异步任务
┌─────────────────────────────────────────┐
│         Celery Worker                    │
│  - 异步AI任务                            │
│  - 批量推理                              │
│  - 定时任务                              │
└─────────────────────────────────────────┘
```

### 3.2 轻量模型（CPU）vs 大模型（GPU）

| 模型类型 | 部署位置 | 推理方式 | 响应时间 |
|---------|---------|---------|---------|
| 情感分析 | FastAPI主服务 | 同步 | <100ms |
| 文本分类 | FastAPI主服务 | 同步 | <100ms |
| 语义搜索 | FastAPI主服务 | 同步 | <50ms |
| 诗词生成(小模型) | FastAPI主服务 | 同步 | 1-2秒 |
| 诗词生成(大模型) | 独立GPU服务 | 异步 | 5-10秒 |

### 3.3 模型优化技术

#### 1. 模型量化（减小模型大小）

```python
from transformers import AutoModelForCausalLM
import torch

# 加载模型时使用量化
model = AutoModelForCausalLM.from_pretrained(
    "model_name",
    load_in_8bit=True,  # 8位量化
    device_map="auto"
)

# 或使用4位量化（需要bitsandbytes）
model = AutoModelForCausalLM.from_pretrained(
    "model_name",
    load_in_4bit=True,
    device_map="auto"
)
```

**效果**：
- 8位量化：模型大小减半，速度提升20-30%
- 4位量化：模型大小1/4，速度提升50%+

#### 2. 批量推理

```python
async def batch_predict(texts: list[str], batch_size: int = 32):
    """批量预测，提高吞吐量"""
    results = []
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        batch_results = model.predict(batch)
        results.extend(batch_results)
    return results
```

#### 3. 模型缓存

```python
from functools import lru_cache

@lru_cache(maxsize=1000)
def generate_poetry_cached(prompt: str, style: str):
    """缓存常见请求"""
    return model.generate(prompt, style)
```

---

## 四、AI功能实施路线图

### 阶段一：基础AI（1-2周）✅

**目标**：实现基础推荐和情感分析

1. 协同过滤推荐（基于用户行为）
2. 情感分析（RoBERTa小模型）
3. 朝代分类（BERT）

**技术要求**：CPU即可

---

### 阶段二：高级AI（2-3周）🚀

**目标**：引入深度学习推荐和语义搜索

1. 深度学习推荐模型
2. 语义搜索（Sentence-BERT + Faiss）
3. OCR识别（PaddleOCR）

**技术要求**：推荐GPU，CPU也可运行

---

### 阶段三：生成AI（2-3周）🤖

**目标**：AI诗词生成

1. GPT-2小模型诗词生成（CPU版）
2. ChatGLM大模型生成（GPU版）
3. 飞花令AI对手

**技术要求**：必须GPU

---

### 阶段四：优化与扩展（持续）💎

1. 模型微调（使用自有数据）
2. A/B测试AI效果
3. 多模态AI（图文结合）
4. 知识图谱构建

---

## 五、总结

### AI能力矩阵

| 功能 | MVP | 成熟期 | 未来 |
|------|-----|--------|------|
| **推荐** | 协同过滤 | 深度学习 | 强化学习 |
| **生成** | GPT-2小模型 | ChatGLM | 微调大模型 |
| **搜索** | 关键词 | 语义搜索 | 多模态搜索 |
| **分析** | 规则引擎 | 深度模型 | 大语言模型 |

### 投入产出比

| 功能 | 开发成本 | 服务器成本 | 用户价值 | ROI |
|------|---------|-----------|---------|-----|
| 智能推荐 | 中 | 低 | ⭐⭐⭐⭐⭐ | 高 |
| 语义搜索 | 中 | 低 | ⭐⭐⭐⭐⭐ | 高 |
| 情感分析 | 低 | 低 | ⭐⭐⭐⭐ | 高 |
| 诗词生成 | 高 | 高 | ⭐⭐⭐⭐⭐ | 中 |
| OCR识别 | 中 | 低 | ⭐⭐⭐ | 中 |

**建议优先级**：
1. ⭐⭐⭐⭐⭐ 智能推荐
2. ⭐⭐⭐⭐⭐ 语义搜索
3. ⭐⭐⭐⭐ 情感分析
4. ⭐⭐⭐⭐ 诗词生成（小模型先行）
5. ⭐⭐⭐ OCR识别

---

**Python + AI = 诗词平台的核心竞争力！** 🤖🎉
