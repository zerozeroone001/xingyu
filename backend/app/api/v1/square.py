from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_optional_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.schemas.square import SquareCommentCreate, SquareTopicCreate
from app.services import square_service

router = APIRouter(prefix="/square", tags=["square"])


@router.get("/feed")
def feed(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> dict:
    return success(square_service.list_feed(db, user, page, page_size))


@router.post("/feed")
def create_topic(payload: SquareTopicCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(square_service.create_topic(db, user, payload))


@router.get("/feed/{topic_id}")
def topic(topic_id: int, db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)) -> dict:
    return success(square_service.get_topic(db, user, topic_id))


@router.post("/feed/{topic_id}/like")
def like_topic(topic_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    square_service.toggle_reaction(db, user, "topic", topic_id, "like")
    return success(square_service.get_topic(db, user, topic_id))


@router.post("/feed/{topic_id}/favorite")
def favorite_topic(topic_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    square_service.toggle_reaction(db, user, "topic", topic_id, "favorite")
    return success(square_service.get_topic(db, user, topic_id))


@router.post("/feed/{topic_id}/share")
def share_topic(topic_id: int, db: Session = Depends(get_db)) -> dict:
    square_service.increase_share(db, topic_id)
    return success(square_service.get_topic(db, None, topic_id))


@router.post("/feed/{topic_id}/comments")
def comment_topic(
    topic_id: int,
    payload: SquareCommentCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    return success(square_service.create_comment(db, user, topic_id, payload))


@router.post("/feed/{topic_id}/comments/{comment_id}/like")
def like_comment(
    topic_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    square_service.toggle_reaction(db, user, "comment", comment_id, "like")
    return success(square_service.get_topic(db, user, topic_id))


@router.post("/feed/{topic_id}/comments/{comment_id}/favorite")
def favorite_comment(
    topic_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    square_service.toggle_reaction(db, user, "comment", comment_id, "favorite")
    return success(square_service.get_topic(db, user, topic_id))
