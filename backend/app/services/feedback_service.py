from __future__ import annotations

from sqlalchemy.orm import Session

from app.db import models
from app.schemas.feedback import FeedbackCreate


def create_feedback(db: Session, user: models.User | None, data: FeedbackCreate) -> dict:
    feedback = models.Feedback(
        user_id=user.id if user else None,
        content=data.content,
        contact=data.contact,
    )
    db.add(feedback)
    db.commit()
    db.refresh(feedback)
    return {
        "id": feedback.id,
        "status": feedback.status,
        "created_at": feedback.created_at.isoformat(),
        "content": feedback.content,
    }
