from __future__ import annotations

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.core.security import create_access_token
from app.db import models
from app.schemas.user import UserUpdate
from app.services.serializers import user_detail


def login_with_wx_code(db: Session, code: str, profile: dict) -> dict:
    # 开发环境先用 code 生成稳定 openid；接入微信时只需要替换这里的 openid 获取逻辑。
    openid = f"mock:{code or 'guest'}"
    user = db.scalar(select(models.User).where(models.User.openid == openid))
    if user is None:
        user = models.User(
            openid=openid,
            nickname=profile.get("nickname") or profile.get("nickName") or "诗词访客",
            avatar_url=profile.get("avatar_url") or profile.get("avatarUrl") or "",
            avatar_text=(profile.get("avatarText") or "诗")[:2],
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    else:
        user.nickname = profile.get("nickname") or profile.get("nickName") or user.nickname
        user.avatar_url = profile.get("avatar_url") or profile.get("avatarUrl") or user.avatar_url
        db.commit()
        db.refresh(user)

    return {
        "token": create_access_token(str(user.id)),
        "user": user_detail(user, get_user_stats(db, user.id)),
    }


def update_user(db: Session, user: models.User, data: UserUpdate) -> dict:
    payload = data.model_dump(exclude_unset=True)
    if "nickname" in payload and payload["nickname"] is not None:
        user.nickname = payload["nickname"]
    if "avatar_url" in payload and payload["avatar_url"] is not None:
        user.avatar_url = payload["avatar_url"]
    avatar_text = payload.get("avatar_text") or payload.get("avatarText")
    if avatar_text:
        user.avatar_text = avatar_text[:2]
    for field in ("title", "gender", "city", "bio"):
        value = payload.get(field)
        if value is not None:
            setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user_detail(user, get_user_stats(db, user.id))


def get_user_stats(db: Session, user_id: int) -> dict[str, int]:
    poems = db.scalar(select(func.count()).select_from(models.SquareTopic).where(models.SquareTopic.user_id == user_id)) or 0
    likes = db.scalar(
        select(func.count()).select_from(models.SquareReaction).where(
            models.SquareReaction.user_id == user_id,
            models.SquareReaction.reaction_type == "like",
        )
    ) or 0
    favorites = db.scalar(select(func.count()).select_from(models.Favorite).where(models.Favorite.user_id == user_id)) or 0
    follows = db.scalar(select(func.count()).select_from(models.UserFollow).where(models.UserFollow.user_id == user_id)) or 0
    return {
        "poem_count": poems,
        "like_count": likes,
        "favorite_count": favorites,
        "following_count": follows,
    }


def get_overview(db: Session, user: models.User) -> dict:
    stats = get_user_stats(db, user.id)
    return {
        "user": user_detail(user, stats),
        "stats": {
            "poems": stats["poem_count"],
            "likes": stats["like_count"],
            "favorites": stats["favorite_count"],
            "follows": stats["following_count"],
        },
    }


def get_profile_items(db: Session, user: models.User, item_type: str, page: int, page_size: int) -> dict:
    from app.services.poem_service import list_favorites
    from app.services.square_service import list_my_topics, list_liked_topics
    from app.utils.pagination import page_dict

    if item_type == "favorites":
        return list_favorites(db, user, page, page_size)
    if item_type == "likes":
        return list_liked_topics(db, user, page, page_size)
    if item_type == "follows":
        follows = db.scalars(
            select(models.UserFollow).where(models.UserFollow.user_id == user.id).offset((page - 1) * page_size).limit(page_size)
        ).all()
        total = db.scalar(select(func.count()).select_from(models.UserFollow).where(models.UserFollow.user_id == user.id)) or 0
        users = [db.get(models.User, follow.target_user_id) for follow in follows]
        items = [
            {
                "id": target.id,
                "kind": "user",
                "title": target.nickname,
                "subtitle": target.title,
                "content": target.bio,
                "badge": "关注",
                "meta": "已关注",
                "avatarText": target.avatar_text,
            }
            for target in users
            if target is not None
        ]
        return page_dict(items, page, page_size, total)
    return list_my_topics(db, user, page, page_size)
