from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str
    app_env: str
    api_v1_prefix: str
    database_url: str
    jwt_secret_key: str
    jwt_expire_minutes: int
    wx_appid: str
    wx_secret: str
    backend_dir: Path
    data_dir: Path

    @property
    def is_dev(self) -> bool:
        return self.app_env.lower() in {"dev", "development", "local"}


def load_settings() -> Settings:
    backend_dir = Path(__file__).resolve().parents[2]
    data_dir = backend_dir / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    database_url = os.getenv("DATABASE_URL", "sqlite:///./data/app.db")

    return Settings(
        app_name=os.getenv("APP_NAME", "xingyu"),
        app_env=os.getenv("APP_ENV", "dev"),
        api_v1_prefix="/api/v1",
        database_url=database_url,
        jwt_secret_key=os.getenv("JWT_SECRET_KEY", "dev-secret-change-me"),
        jwt_expire_minutes=int(os.getenv("JWT_EXPIRE_MINUTES", "10080")),
        wx_appid=os.getenv("WX_APPID", ""),
        wx_secret=os.getenv("WX_SECRET", ""),
        backend_dir=backend_dir,
        data_dir=data_dir,
    )


settings = load_settings()
