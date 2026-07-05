from __future__ import annotations

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.api.deps import get_optional_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.schemas.feedback import FeedbackCreate
from app.services.feedback_service import create_feedback

router = APIRouter(prefix="/feedback", tags=["feedback"])


@router.post("")
def feedback(payload: FeedbackCreate, db: Session = Depends(get_db), user: User | None = Depends(get_optional_user)) -> dict:
    return success(create_feedback(db, user, payload))
