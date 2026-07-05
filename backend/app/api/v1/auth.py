from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.schemas.auth import WxLoginRequest
from app.services.user_service import login_with_wx_code

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/wx-login")
def wx_login(payload: WxLoginRequest, db: Session = Depends(get_db)) -> dict:
    return success(login_with_wx_code(db, payload.code, payload.profile))


@router.post("/logout")
def logout(_: User = Depends(get_current_user)) -> dict:
    return success({"logged_out": True})
