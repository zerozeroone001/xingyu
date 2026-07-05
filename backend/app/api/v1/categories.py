from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_optional_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.services.poem_service import list_categories, list_category_poems

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("")
def categories(db: Session = Depends(get_db)) -> dict:
    return success(list_categories(db))


@router.get("/{category_id}/poems")
def category_poems(
    category_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User | None = Depends(get_optional_user),
) -> dict:
    return success(list_category_poems(db, category_id, user, page, page_size))
