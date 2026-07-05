from __future__ import annotations

from fastapi import Depends
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.orm import Session

from app.core.exceptions import BusinessError
from app.core.security import decode_access_token
from app.db.models import User
from app.db.session import get_db

bearer_scheme = HTTPBearer(auto_error=False)


def get_current_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User:
    if credentials is None:
        raise BusinessError("请先登录", code=40100, status_code=401)
    payload = decode_access_token(credentials.credentials)
    user_id = int(payload.get("sub", 0) or 0)
    user = db.get(User, user_id)
    if user is None:
        raise BusinessError("用户不存在", code=40103, status_code=401)
    return user


def get_optional_user(
    db: Session = Depends(get_db),
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> User | None:
    if credentials is None:
        return None
    try:
        payload = decode_access_token(credentials.credentials)
    except BusinessError:
        return None
    user_id = int(payload.get("sub", 0) or 0)
    return db.get(User, user_id)
