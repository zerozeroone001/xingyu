from __future__ import annotations

import os
from typing import Any

from fastapi import APIRouter, Depends, Query
from fastapi.security import HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from app.api.deps import bearer_scheme
from app.core.exceptions import BusinessError
from app.core.response import success
from app.core.security import create_access_token, decode_access_token
from app.db.session import get_db
from app.schemas.admin import (
    AdminLoginRequest,
    CategoryAdminPayload,
    FeihualingRoomAdminPayload,
    FeedbackAdminPayload,
    PoemAdminPayload,
    SquareTopicAdminPayload,
    UserAdminPayload,
)
from app.services import admin_service

router = APIRouter(prefix="/admin", tags=["admin"])


def require_admin(credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme)) -> dict[str, Any]:
    if credentials is None:
        raise BusinessError("Admin login required", code=40110, status_code=401)
    payload = decode_access_token(credentials.credentials)
    if payload.get("role") != "admin":
        raise BusinessError("Admin permission required", code=40310, status_code=403)
    return payload


@router.post("/auth/login")
def login(payload: AdminLoginRequest) -> dict:
    username = os.getenv("ADMIN_USERNAME", "admin")
    password = os.getenv("ADMIN_PASSWORD", "admin123456")
    if payload.username != username or payload.password != password:
        raise BusinessError("Invalid admin username or password", code=40111, status_code=401)
    token = create_access_token(f"admin:{username}", {"role": "admin", "username": username})
    return success({"token": token, "username": username})


@router.get("/dashboard")
def dashboard(_: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.dashboard(db))


@router.get("/poems")
def poems(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = "",
    dynasty: str = "",
    author: str = "",
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    return success(admin_service.list_poems(db, page, page_size, keyword, dynasty, author))


@router.post("/poems")
def create_poem(payload: PoemAdminPayload, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.create_poem(db, payload))


@router.put("/poems/{poem_id}")
def update_poem(poem_id: int, payload: PoemAdminPayload, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.update_poem(db, poem_id, payload))


@router.delete("/poems/{poem_id}")
def delete_poem(poem_id: int, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.delete_poem(db, poem_id))


@router.get("/categories")
def categories(_: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.list_categories(db))


@router.post("/categories")
def create_category(payload: CategoryAdminPayload, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.create_category(db, payload))


@router.put("/categories/{category_id}")
def update_category(category_id: int, payload: CategoryAdminPayload, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.update_category(db, category_id, payload))


@router.delete("/categories/{category_id}")
def delete_category(category_id: int, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.delete_category(db, category_id))


@router.get("/users")
def users(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = "",
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    return success(admin_service.list_users(db, page, page_size, keyword))


@router.put("/users/{user_id}")
def update_user(user_id: int, payload: UserAdminPayload, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.update_user(db, user_id, payload))


@router.get("/square/topics")
def topics(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = "",
    user_id: int | None = None,
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    return success(admin_service.list_topics(db, page, page_size, keyword, user_id))


@router.put("/square/topics/{topic_id}")
def update_topic(topic_id: int, payload: SquareTopicAdminPayload, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.update_topic(db, topic_id, payload))


@router.delete("/square/topics/{topic_id}")
def delete_topic(topic_id: int, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.delete_topic(db, topic_id))


@router.get("/square/comments")
def comments(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = "",
    topic_id: int | None = None,
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    return success(admin_service.list_comments(db, page, page_size, keyword, topic_id))


@router.delete("/square/comments/{comment_id}")
def delete_comment(comment_id: int, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.delete_comment(db, comment_id))


@router.get("/feedback")
def feedback(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status: str = "",
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    return success(admin_service.list_feedback(db, page, page_size, status))


@router.put("/feedback/{feedback_id}")
def update_feedback(feedback_id: int, payload: FeedbackAdminPayload, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.update_feedback(db, feedback_id, payload))


@router.delete("/feedback/{feedback_id}")
def delete_feedback(feedback_id: int, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.delete_feedback(db, feedback_id))


@router.get("/feihualing/rooms")
def rooms(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = "",
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    return success(admin_service.list_rooms(db, page, page_size, keyword))


@router.put("/feihualing/rooms/{room_id}")
def update_room(room_id: int, payload: FeihualingRoomAdminPayload, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.update_room(db, room_id, payload))


@router.delete("/feihualing/rooms/{room_id}")
def delete_room(room_id: int, _: dict = Depends(require_admin), db: Session = Depends(get_db)) -> dict:
    return success(admin_service.delete_room(db, room_id))


@router.get("/feihualing/records")
def records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str = "",
    _: dict = Depends(require_admin),
    db: Session = Depends(get_db),
) -> dict:
    return success(admin_service.list_records(db, page, page_size, keyword))


@router.get("/system/health")
def system_health(_: dict = Depends(require_admin)) -> dict:
    return success({"api": "ok"})
