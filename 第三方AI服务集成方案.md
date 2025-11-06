# 诗词程序 - 第三方AI服务集成方案

> **注意**：本方案采用调用第三方AI厂商API的方式，**无需本地部署模型**，大幅降低开发和运维成本。

---

## 一、方案优势

### ✅ 对比本地部署的优势

| 对比项 | 本地部署AI模型 | 调用第三方API |
|-------|--------------|-------------|
| **开发成本** | 高（需要AI专业知识） | 低（调用API即可） |
| **服务器成本** | 高（需GPU服务器，1000+元/月） | 低（普通服务器200元/月） |
| **维护成本** | 高（模型更新、优化） | 低（厂商负责） |
| **启动速度** | 慢（模型加载） | 快（API调用） |
| **模型质量** | 需自己训练/微调 | 厂商持续优化 |
| **扩展性** | 受限于服务器性能 | 按需扩展 |
| **技术门槛** | 高 | 低 |
| **API调用费用** | 无 | 有（按量计费） |

**结论**：对于MVP阶段和中小型项目，**调用第三方API性价比更高**。

---

## 二、国内主流AI服务商对比

### 2.1 服务商选择

| 服务商 | 模型 | 适用场景 | 定价 | 推荐指数 |
|-------|------|---------|------|---------|
| **阿里云-通义千问** | 通义千问-Turbo/Plus/Max | 通用对话、文本生成 | 0.0008-0.12元/千tokens | ⭐⭐⭐⭐⭐ |
| **百度-文心一言** | ERNIE-Bot-Turbo/4.0 | 中文理解、内容创作 | 0.008-0.12元/千tokens | ⭐⭐⭐⭐⭐ |
| **讯飞-星火** | 星火认知大模型 | 中文对话、知识问答 | 免费额度+付费 | ⭐⭐⭐⭐ |
| **智谱AI** | ChatGLM-Turbo/Pro | 对话、文本生成 | 0.005-0.1元/千tokens | ⭐⭐⭐⭐ |
| **腾讯-混元** | 混元大模型 | 通用对话 | 内测中 | ⭐⭐⭐⭐ |
| **Minimax** | abab6-chat | 对话、创作 | 0.015元/千tokens | ⭐⭐⭐ |

### 2.2 推荐方案

**主力模型**：**阿里云通义千问** 或 **百度文心一言**

**理由**：
1. ✅ 中文能力强，特别适合诗词场景
2. ✅ API稳定，文档完善
3. ✅ 价格合理，有免费额度
4. ✅ 大厂背书，服务可靠
5. ✅ 功能丰富（对话、生成、理解）

---

## 三、核心AI功能实现

### 3.1 智能推荐 🎯

**方案**：前期使用**协同过滤**（不依赖AI），后期可调用AI做个性化推荐

```python
# 基础推荐：协同过滤（无需AI）
class BasicRecommender:
    """基于用户行为的协同过滤推荐"""

    async def recommend(self, user_id: int, top_k: int = 10):
        """
        推荐逻辑：
        1. 找相似用户（点赞、收藏相似）
        2. 推荐相似用户喜欢的诗词
        3. 结合热度、时间等因素
        """
        # 不需要调用AI API
        pass

# 进阶推荐：调用AI（可选）
class AIRecommender:
    """基于AI的个性化推荐"""

    async def recommend_with_ai(self, user_profile: dict):
        """
        调用AI分析用户偏好
        - 输入：用户浏览历史、喜好描述
        - 输出：推荐理由
        """
        prompt = f"""
        用户画像：{user_profile}
        请从以下诗词中推荐最适合该用户的5首，并说明理由。
        """
        result = await self.call_ai_api(prompt)
        return result
```

**推荐**：MVP阶段使用协同过滤，**不调用AI**，成本低效果好。

---

### 3.2 AI诗词生成 ✍️

**方案**：调用**通义千问**或**文心一言**生成诗词

#### 实现代码

```python
import httpx
from typing import Optional

class PoetryAIGenerator:
    """调用第三方AI生成诗词"""

    def __init__(self):
        # 选择服务商（这里以通义千问为例）
        self.api_key = "your-api-key"  # 从环境变量读取
        self.api_url = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation"

    async def generate_poetry(
        self,
        prompt: str,
        style: str = "五言绝句",
        dynasty: str = "唐代",
        author_style: Optional[str] = None
    ) -> dict:
        """
        AI生成诗词

        Args:
            prompt: 主题，如"明月"、"春天"
            style: 诗词体裁，如"五言绝句"、"七言律诗"
            dynasty: 朝代风格，如"唐代"、"宋代"
            author_style: 诗人风格（可选），如"李白"、"杜甫"

        Returns:
            {
                "poetry": "生成的诗词",
                "title": "诗词标题（可选）",
                "explanation": "创作说明"
            }
        """
        # 构造提示词
        system_prompt = """你是一位精通中国古典诗词的AI诗人。
        请根据用户提供的主题和要求，创作一首优美的诗词。
        要求：
        1. 符合指定的诗词体裁和格律
        2. 意境优美，富有诗意
        3. 用词典雅，符合古典诗词风格
        """

        user_prompt = f"""
        主题：{prompt}
        体裁：{style}
        朝代风格：{dynasty}
        """

        if author_style:
            user_prompt += f"\n诗人风格：模仿{author_style}的风格"

        user_prompt += f"\n\n请创作一首{style}，主题围绕"{prompt}"。"

        # 调用API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.api_url,
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "qwen-turbo",  # 或 qwen-plus、qwen-max
                    "input": {
                        "messages": [
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_prompt}
                        ]
                    },
                    "parameters": {
                        "temperature": 0.8,  # 创造性
                        "top_p": 0.95,
                        "max_tokens": 500
                    }
                },
                timeout=30.0
            )

        if response.status_code == 200:
            result = response.json()
            poetry_text = result['output']['text']

            # 解析诗词（根据返回格式调整）
            return {
                "poetry": poetry_text,
                "title": self._extract_title(poetry_text),
                "explanation": "AI创作"
            }
        else:
            raise Exception(f"API调用失败: {response.text}")

    def _extract_title(self, text: str) -> str:
        """从生成的文本中提取标题"""
        # 简单实现：取第一行或让AI返回JSON格式
        lines = text.strip().split('\n')
        return lines[0] if lines else "无题"


# FastAPI接口
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/ai", tags=["AI"])

class PoetryGenerateRequest(BaseModel):
    prompt: str
    style: str = "五言绝句"
    dynasty: str = "唐代"
    author_style: Optional[str] = None

@router.post("/generate-poetry")
async def generate_poetry(request: PoetryGenerateRequest):
    """
    AI生成诗词

    示例请求：
    {
        "prompt": "明月",
        "style": "五言绝句",
        "dynasty": "唐代",
        "author_style": "李白"
    }

    示例响应：
    {
        "poetry": "明月照高楼，\n流光正徘徊。\n上有愁思妇，\n悲叹有余哀。",
        "title": "月夜",
        "explanation": "AI创作"
    }
    """
    try:
        generator = PoetryAIGenerator()
        result = await generator.generate_poetry(
            prompt=request.prompt,
            style=request.style,
            dynasty=request.dynasty,
            author_style=request.author_style
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

#### 成本估算

**通义千问定价**（2024年）：
- qwen-turbo: 0.0008元/千tokens（输入），0.002元/千tokens（输出）
- qwen-plus: 0.004元/千tokens（输入），0.008元/千tokens（输出）
- qwen-max: 0.04元/千tokens（输入），0.12元/千tokens（输出）

**一次诗词生成**：
- 输入：约200 tokens（提示词）
- 输出：约100 tokens（诗词）
- 成本：约 0.0001元（使用qwen-turbo）

**月成本**（1万次生成）：约 **1-2元**

---

### 3.3 诗词理解与分析 📖

**功能**：
- 诗词翻译（文言文→现代文）
- 情感分析
- 赏析生成

```python
class PoetryAnalyzer:
    """诗词分析服务"""

    async def analyze_poetry(self, poetry_content: str) -> dict:
        """
        分析诗词

        Returns:
            {
                "translation": "现代文翻译",
                "emotion": "情感分析",
                "appreciation": "赏析",
                "keywords": ["关键词"]
            }
        """
        prompt = f"""
        请分析以下诗词：

        {poetry_content}

        请提供：
        1. 现代文翻译
        2. 情感分析（如：思乡、豪迈、婉约等）
        3. 简要赏析（100字以内）
        4. 关键词（3-5个）

        请以JSON格式返回：
        {{
            "translation": "...",
            "emotion": "...",
            "appreciation": "...",
            "keywords": ["...", "..."]
        }}
        """

        result = await self.call_ai_api(prompt)
        return result

@router.post("/analyze-poetry")
async def analyze_poetry(poetry_content: str):
    """诗词分析"""
    analyzer = PoetryAnalyzer()
    result = await analyzer.analyze_poetry(poetry_content)
    return result
```

---

### 3.4 智能搜索 🔍

**方案一**：传统关键词搜索（Elasticsearch）**不需要AI**

**方案二**：语义搜索（调用AI理解用户意图）

```python
class SemanticSearch:
    """AI语义搜索"""

    async def search(self, query: str) -> list:
        """
        用户输入："描写春天的诗"
        AI理解意图 → 生成搜索关键词 → Elasticsearch检索
        """
        # 1. 调用AI理解用户意图
        prompt = f"""
        用户搜索：{query}

        请分析用户的搜索意图，提取以下信息：
        1. 主题词（如：春天、爱情、思乡）
        2. 情感（如：喜悦、悲伤）
        3. 朝代（如：唐代、宋代）
        4. 诗人（如果提到）

        以JSON格式返回：
        {{
            "theme": ["..."],
            "emotion": "...",
            "dynasty": "...",
            "poet": "..."
        }}
        """

        ai_result = await self.call_ai_api(prompt)

        # 2. 根据AI分析结果，构建Elasticsearch查询
        es_query = self.build_es_query(ai_result)

        # 3. 执行搜索
        results = await self.es_client.search(query=es_query)

        return results
```

**推荐**：MVP阶段使用Elasticsearch关键词搜索，**不调用AI**。后期优化再考虑。

---

### 3.5 飞花令AI对手 🎮

```python
class FeiHuaLingAI:
    """飞花令AI对手"""

    async def generate_response(
        self,
        keyword: str,
        history: list[str]
    ) -> str:
        """
        生成飞花令诗句

        Args:
            keyword: 关键字，如"春"
            history: 已使用的诗句列表

        Returns:
            包含关键字的诗句
        """
        prompt = f"""
        这是一场飞花令游戏，关键字是"{keyword}"。

        已使用的诗句：
        {chr(10).join(history)}

        请说出一句包含"{keyword}"字的古诗词，要求：
        1. 不能重复已使用的诗句
        2. 必须是真实的古诗词
        3. 只返回诗句，不要其他说明
        """

        poetry_line = await self.call_ai_api(prompt)

        # 验证是否包含关键字
        if keyword not in poetry_line:
            raise ValueError("AI返回的诗句不包含关键字")

        return poetry_line

@router.post("/game/feihualing-ai")
async def feihualing_ai_response(keyword: str, history: list[str]):
    """飞花令AI对手"""
    ai = FeiHuaLingAI()
    response = await ai.generate_response(keyword, history)
    return {"poetry_line": response}
```

---

### 3.6 智能问答 💬

```python
class PoetryQA:
    """诗词知识问答"""

    async def answer_question(self, question: str) -> str:
        """
        回答诗词相关问题

        示例：
        - "李白写过哪些有名的诗？"
        - "什么是律诗？"
        - "唐诗和宋词有什么区别？"
        """
        # 可以结合RAG（检索增强生成）
        # 1. 从数据库检索相关知识
        relevant_docs = await self.search_knowledge(question)

        # 2. 构造提示词
        prompt = f"""
        用户问题：{question}

        相关知识：
        {relevant_docs}

        请根据相关知识回答用户问题，要求：
        1. 准确、专业
        2. 简洁明了
        3. 如果涉及具体诗词，可以引用
        """

        answer = await self.call_ai_api(prompt)
        return answer

@router.post("/ai/qa")
async def poetry_qa(question: str):
    """诗词知识问答"""
    qa = PoetryQA()
    answer = await qa.answer_question(question)
    return {"answer": answer}
```

---

## 四、多厂商支持（适配器模式）

为了避免被单一厂商锁定，建议使用**适配器模式**支持多个AI服务商。

```python
from abc import ABC, abstractmethod

class AIProvider(ABC):
    """AI服务商抽象接口"""

    @abstractmethod
    async def chat(self, messages: list, **kwargs) -> str:
        """对话接口"""
        pass

    @abstractmethod
    async def generate(self, prompt: str, **kwargs) -> str:
        """文本生成接口"""
        pass


class TongYiProvider(AIProvider):
    """阿里通义千问"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.api_url = "https://dashscope.aliyuncs.com/..."

    async def chat(self, messages: list, **kwargs) -> str:
        # 调用通义千问API
        pass

    async def generate(self, prompt: str, **kwargs) -> str:
        pass


class WenXinProvider(AIProvider):
    """百度文心一言"""

    def __init__(self, api_key: str, secret_key: str):
        self.api_key = api_key
        self.secret_key = secret_key
        self.api_url = "https://aip.baidubce.com/..."

    async def chat(self, messages: list, **kwargs) -> str:
        # 调用文心一言API
        pass

    async def generate(self, prompt: str, **kwargs) -> str:
        pass


class AIService:
    """AI服务（统一接口）"""

    def __init__(self, provider: AIProvider):
        self.provider = provider

    async def generate_poetry(self, prompt: str, **kwargs):
        result = await self.provider.generate(prompt, **kwargs)
        return result


# 使用
# 方式1：使用通义千问
ai_service = AIService(TongYiProvider(api_key="xxx"))

# 方式2：使用文心一言
ai_service = AIService(WenXinProvider(api_key="xxx", secret_key="yyy"))

# 方式3：从配置文件读取
provider_name = config.AI_PROVIDER  # "tongyi" or "wenxin"
if provider_name == "tongyi":
    provider = TongYiProvider(api_key=config.TONGYI_API_KEY)
elif provider_name == "wenxin":
    provider = WenXinProvider(api_key=config.WENXIN_API_KEY, secret_key=config.WENXIN_SECRET_KEY)

ai_service = AIService(provider)
```

---

## 五、项目目录结构（简化版）

```
server/  (Python FastAPI - 无需本地AI模型)
├── app/
│   ├── main.py
│   ├── core/
│   │   ├── config.py         # 配置（包含API密钥）
│   │   ├── security.py
│   │   └── database.py
│   ├── models/               # SQLAlchemy模型
│   ├── schemas/              # Pydantic模型
│   ├── api/v1/
│   │   ├── auth.py
│   │   ├── poetry.py
│   │   ├── ai.py             # AI接口
│   │   └── ...
│   ├── services/
│   │   ├── ai_service.py     # AI服务（调用第三方API）✨
│   │   │   ├── providers/    # AI服务商适配器
│   │   │   │   ├── tongyi.py     # 通义千问
│   │   │   │   ├── wenxin.py     # 文心一言
│   │   │   │   └── base.py       # 抽象基类
│   │   │   ├── poetry_generator.py  # 诗词生成
│   │   │   ├── poetry_analyzer.py   # 诗词分析
│   │   │   └── poetry_qa.py         # 知识问答
│   │   ├── recommender_service.py  # 推荐服务（协同过滤）
│   │   └── search_service.py       # 搜索服务（ES）
│   ├── tasks/                # Celery任务
│   ├── websocket/            # WebSocket
│   └── utils/
├── requirements.txt          # 依赖（不需要torch、transformers）✨
├── .env
└── README.md
```

**关键变化**：
- ✅ 移除 `ai/models/` 目录（不需要存储模型文件）
- ✅ 移除 `notebooks/` 目录（不需要训练模型）
- ✅ 简化 AI 模块（只需要调用API的代码）
- ✅ 依赖包大幅减少

---

## 六、依赖包（简化版）

```txt
# requirements.txt

# Web框架
fastapi==0.104.1
uvicorn[standard]==0.24.0

# 数据库
sqlalchemy==2.0.23
aiomysql==0.2.0

# Redis
redis==5.0.1

# HTTP客户端（调用AI API）
httpx==0.25.1  # 异步HTTP客户端

# 认证
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4

# 任务队列
celery==5.3.4

# Elasticsearch
elasticsearch==8.11.0

# 工具
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0

# ❌ 不需要以下依赖：
# torch==2.1.0  # 移除
# transformers==4.35.0  # 移除
# sentence-transformers==2.2.2  # 移除
# paddleocr==2.7.0  # 移除
# scikit-learn==1.3.2  # 可选（如需协同过滤）
```

**依赖包大小对比**：
- 本地AI模型方案：~5GB（PyTorch + 模型文件）
- 第三方API方案：~100MB（仅基础依赖）

---

## 七、成本分析

### 7.1 服务器成本（月）

| 项目 | 本地AI方案 | 第三方API方案 |
|------|-----------|-------------|
| Web服务器 | 2核4G，100元 | 2核4G，100元 |
| GPU服务器 | **1000-2000元** | **无需** ❌ |
| MySQL | 50元 | 50元 |
| Redis | 30元 | 30元 |
| **总计** | **1180-2180元** | **180-200元** ✅ |

**节省**：约 **1000-2000元/月**

### 7.2 AI API调用成本（月）

假设每月用户量：
- 诗词生成：1000次
- 诗词分析：5000次
- 问答：2000次

**通义千问（qwen-turbo）**：
- 诗词生成：1000次 × 0.0003元 = 0.3元
- 诗词分析：5000次 × 0.0002元 = 1元
- 问答：2000次 × 0.0003元 = 0.6元
- **总计**：约 **2元/月**

**即使用户量增长10倍**，AI调用成本也仅 **20元/月**，远低于GPU服务器成本。

### 7.3 总成本对比

| 方案 | 月成本 | 适用规模 |
|------|--------|---------|
| **第三方API方案** | **200-220元** | 初创、中小型项目 ✅ |
| **本地AI方案** | **1200-2200元** | 大型项目、特殊需求 |

**结论**：对于绝大多数项目，**第三方API方案性价比更高**。

---

## 八、申请API密钥指南

### 8.1 阿里云通义千问

**步骤**：
1. 访问：https://dashscope.aliyun.com/
2. 登录/注册阿里云账号
3. 进入控制台 → 创建API密钥
4. 新用户有**免费额度**（100万tokens）

**定价**：https://help.aliyun.com/zh/model-studio/pricing

### 8.2 百度文心一言

**步骤**：
1. 访问：https://cloud.baidu.com/product/wenxinworkshop
2. 登录百度智能云
3. 开通文心一言服务
4. 创建应用，获取API Key和Secret Key

**免费额度**：每月赠送一定tokens

### 8.3 讯飞星火

**步骤**：
1. 访问：https://xinghuo.xfyun.cn/
2. 注册讯飞开放平台账号
3. 创建应用
4. 获取APPID、APISecret、APIKey

**免费额度**：新用户有免费额度

---

## 九、配置文件

```python
# app/core/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # 基础配置
    APP_NAME: str = "诗词平台"
    DEBUG: bool = False

    # 数据库
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # AI服务配置
    AI_PROVIDER: str = "tongyi"  # tongyi, wenxin, xinghuo

    # 通义千问
    TONGYI_API_KEY: str = ""
    TONGYI_MODEL: str = "qwen-turbo"  # qwen-turbo, qwen-plus, qwen-max

    # 文心一言
    WENXIN_API_KEY: str = ""
    WENXIN_SECRET_KEY: str = ""
    WENXIN_MODEL: str = "ernie-bot-turbo"

    # 讯飞星火
    XINGHUO_APPID: str = ""
    XINGHUO_API_SECRET: str = ""
    XINGHUO_API_KEY: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
```

```bash
# .env
AI_PROVIDER=tongyi

# 通义千问
TONGYI_API_KEY=sk-xxxxxxxxxxxxx
TONGYI_MODEL=qwen-turbo

# 文心一言（备用）
WENXIN_API_KEY=xxxxxxxxxxxxx
WENXIN_SECRET_KEY=xxxxxxxxxxxxx
```

---

## 十、开发优先级

### 阶段一（2-3周）：基础功能（无AI）✅

1. 用户登录注册
2. 诗词列表、详情
3. 搜索（Elasticsearch关键词搜索）
4. 评论、点赞、收藏
5. 推荐（协同过滤）

**AI功能**：暂不接入

### 阶段二（1-2周）：接入AI功能 🤖

1. **AI诗词生成**（核心功能）
   - 接入通义千问
   - 实现诗词生成接口
   - 前端调用展示

2. **诗词分析**
   - 翻译、赏析
   - 情感分析

3. **飞花令AI对手**
   - 实现AI对战逻辑

### 阶段三（持续优化）💎

1. 优化提示词（Prompt Engineering）
2. 缓存热门请求（Redis）
3. 成本优化（使用更便宜的模型）
4. 用户反馈与迭代

---

## 十一、注意事项

### 11.1 API调用限制

- **QPS限制**：通义千问免费版 QPS=2（每秒2次请求）
- **速率限制**：合理控制调用频率
- **超时处理**：设置超时时间（30秒）
- **错误重试**：实现重试机制

### 11.2 成本控制

1. **缓存策略**
   - 相同请求缓存结果（Redis）
   - 降低重复调用

2. **提示词优化**
   - 精简提示词，减少tokens消耗
   - 使用更便宜的模型（qwen-turbo而非qwen-max）

3. **限流策略**
   - 用户每日生成次数限制
   - 防止恶意刷量

### 11.3 数据安全

- ❌ 不要在日志中记录API密钥
- ✅ 使用环境变量存储密钥
- ✅ 用户生成的内容需审核

---

## 十二、总结

### ✅ 推荐方案

```
前端：uni-app (Vue 3) + Element Plus
后端：Python FastAPI + SQLAlchemy
AI：调用第三方API（通义千问/文心一言）✨
数据库：MySQL + Redis + Elasticsearch
```

### 📊 优势总结

| 指标 | 评分 |
|------|------|
| **开发成本** | ⭐⭐⭐⭐⭐ 低 |
| **运维成本** | ⭐⭐⭐⭐⭐ 低 |
| **技术门槛** | ⭐⭐⭐⭐⭐ 低 |
| **扩展性** | ⭐⭐⭐⭐ 好 |
| **AI效果** | ⭐⭐⭐⭐⭐ 优秀 |
| **总成本** | **200-250元/月** |

### 🚀 下一步

1. 申请通义千问或文心一言API密钥
2. 搭建FastAPI项目框架
3. 实现基础功能（无AI）
4. 接入AI诗词生成功能
5. 测试与优化

---

**第三方AI API = 低成本 + 高质量 + 易维护** 🎉
