from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.schemas.user import UserUpdate
from app.services import user_service
from app.services.serializers import user_detail

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me")
def me(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(user_detail(user, user_service.get_user_stats(db, user.id)))


@router.put("/me")
def update_me(payload: UserUpdate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(user_service.update_user(db, user, payload))


@router.get("/me/overview")
def overview(db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(user_service.get_overview(db, user))


@router.get("/me/{item_type}")
def profile_items(
    item_type: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    return success(user_service.get_profile_items(db, user, item_type, page, page_size))
