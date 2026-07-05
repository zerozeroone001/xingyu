from __future__ import annotations

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.core.response import success
from app.db.models import User
from app.db.session import get_db
from app.schemas.feihualing import FeihualingCheckRequest, FeihualingRecordCreate, FeihualingRoomCreate
from app.services import feihualing_service

router = APIRouter(prefix="/feihualing", tags=["feihualing"])


@router.get("/keywords")
def keywords(db: Session = Depends(get_db)) -> dict:
    return success(feihualing_service.keywords(db))


@router.post("/check")
def check(payload: FeihualingCheckRequest, db: Session = Depends(get_db)) -> dict:
    return success(feihualing_service.check_answer(db, payload))


@router.get("/records")
def records(
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
) -> dict:
    return success(feihualing_service.list_records(db, user, page, page_size))


@router.post("/records")
def save_record(payload: FeihualingRecordCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(feihualing_service.save_record(db, user, payload))


@router.get("/rooms")
def rooms(db: Session = Depends(get_db)) -> dict:
    return success(feihualing_service.list_rooms(db))


@router.post("/rooms")
def create_room(payload: FeihualingRoomCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> dict:
    return success(feihualing_service.create_room(db, user, payload))


@router.get("/rooms/{room_id}")
def room(room_id: int, db: Session = Depends(get_db)) -> dict:
    return success(feihualing_service.get_room(db, room_id))
