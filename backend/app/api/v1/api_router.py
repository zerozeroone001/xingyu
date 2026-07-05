from __future__ import annotations

from fastapi import APIRouter

from app.api.v1 import admin, auth, categories, feedback, favorites, feihualing, history, home, poems, square, users
from app.core.response import success

api_router = APIRouter()


@api_router.get("/health", tags=["health"])
def health() -> dict:
    return success({"status": "ok"})


api_router.include_router(auth.router)
api_router.include_router(admin.router)
api_router.include_router(users.router)
api_router.include_router(home.router)
api_router.include_router(poems.router)
api_router.include_router(categories.router)
api_router.include_router(favorites.router)
api_router.include_router(history.router)
api_router.include_router(square.router)
api_router.include_router(feihualing.router)
api_router.include_router(feedback.router)
