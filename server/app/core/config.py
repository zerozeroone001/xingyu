"""
应用配置管理
使用 Pydantic Settings 管理环境变量
"""

from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """应用配置"""

    # 基础配置
    APP_NAME: str = "星语诗词平台"
    APP_ENV: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = "poetry-secret-key-change-in-production-2024"
    HOST: str = "0.0.0.0"
    PORT: int = 8000

    # 数据库配置
    DATABASE_URL: str = "mysql+aiomysql://root:poetry_root_2024@mysql:3306/poetry_db"
    REDIS_URL: str = "redis://redis:6379/0"
    ELASTICSEARCH_URL: str = "http://elasticsearch:9200"

    # JWT配置
    JWT_SECRET_KEY: str = "poetry-jwt-secret-key-2024"
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_TOKEN_EXPIRE_MINUTES: int = 10080  # 7天

    # 微信小程序配置
    WECHAT_APPID: str = ""
    WECHAT_SECRET: str = ""

    # 阿里云OSS配置
    OSS_ACCESS_KEY_ID: str = ""
    OSS_ACCESS_KEY_SECRET: str = ""
    OSS_BUCKET: str = ""
    OSS_ENDPOINT: str = ""

    # AI服务配置
    AI_PROVIDER: str = "tongyi"  # tongyi, wenxin

    # 通义千问配置
    TONGYI_API_KEY: str = ""
    TONGYI_MODEL: str = "qwen-turbo"

    # 文心一言配置
    WENXIN_API_KEY: str = ""
    WENXIN_SECRET_KEY: str = ""

    # CORS配置
    CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8080",
    ]

    # 限流配置
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


# 创建全局配置实例
settings = Settings()
