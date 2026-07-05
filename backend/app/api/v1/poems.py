from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_optional_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.services import poem_service

router = APIRouter(prefix="/poems", tags=["poems"])


@router.get("")
def list_poems(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    keyword: str | None = None,
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> dict:
    return success(poem_service.list_poems(db, user, page, page_size, keyword))


@router.get("/search")
def search_poems(
    keyword: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> dict:
    return success(poem_service.list_poems(db, user, page, page_size, keyword))


@router.get("/{poem_id}")
def poem_detail(poem_id: int, db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)) -> dict:
    return success(poem_service.get_poem_detail(db, poem_id, user))


@router.post("/{poem_id}/like")
def like_poem(poem_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(poem_service.set_like(db, user, poem_id, True))


@router.delete("/{poem_id}/like")
def unlike_poem(poem_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(poem_service.set_like(db, user, poem_id, False))


@router.post("/{poem_id}/share")
def share_poem(poem_id: int, db: Session = Depends(get_db)) -> dict:
    return success(poem_service.increase_share(db, poem_id))
