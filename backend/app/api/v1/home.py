from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_optional_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.services.poem_service import home_data

router = APIRouter(prefix="/home", tags=["home"])


@router.get("")
def get_home(db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)) -> dict:
    return success(home_data(db, user))
