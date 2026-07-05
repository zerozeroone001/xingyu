from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.services import poem_service

router = APIRouter(prefix="/favorites", tags=["favorites"])


@router.get("")
def favorites(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    return success(poem_service.list_favorites(db, user, page, page_size))


@router.post("/{poem_id}")
def add_favorite(poem_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(poem_service.add_favorite(db, user, poem_id))


@router.delete("/{poem_id}")
def remove_favorite(poem_id: int, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(poem_service.remove_favorite(db, user, poem_id))
