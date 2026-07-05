from __future__ import annotations

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.cache import cache
from app.core.exceptions import BusinessError
from app.db import models
from app.schemas.square import SquareCommentCreate, SquareTopicCreate
from app.services.serializers import square_topic_item
from app.utils.json_util import dump_json_list
from app.utils.pagination import page_dict, paginate_select


def _reaction_ids(db: Session, user: models.User | None, target_type: str, reaction_type: str) -> set[int]:
    if user is None:
        return set()
    return set(
        db.scalars(
            select(models.SquareReaction.target_id).where(
                models.SquareReaction.user_id == user.id,
                models.SquareReaction.target_type == target_type,
                models.SquareReaction.reaction_type == reaction_type,
            )
        ).all()
    )


def list_feed(db: Session, user: models.User | None, page: int, page_size: int) -> dict:
    stmt = (
        select(models.SquareTopic)
        .options(selectinload(models.SquareTopic.author), selectinload(models.SquareTopic.comments).selectinload(models.SquareComment.author))
        .order_by(models.SquareTopic.created_at.desc())
    )
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    topic_likes = _reaction_ids(db, user, "topic", "like")
    topic_favorites = _reaction_ids(db, user, "topic", "favorite")
    comment_likes = _reaction_ids(db, user, "comment", "like")
    comment_favorites = _reaction_ids(db, user, "comment", "favorite")
    return page_dict(
        [square_topic_item(row, topic_likes, topic_favorites, comment_likes, comment_favorites) for row in rows],
        page,
        page_size,
        total,
    )


def get_topic(db: Session, user: models.User | None, topic_id: int) -> dict:
    topic = db.scalar(
        select(models.SquareTopic)
        .options(selectinload(models.SquareTopic.author), selectinload(models.SquareTopic.comments).selectinload(models.SquareComment.author))
        .where(models.SquareTopic.id == topic_id)
    )
    if topic is None:
        raise BusinessError("内容不存在", code=40403, status_code=404)
    return square_topic_item(
        topic,
        _reaction_ids(db, user, "topic", "like"),
        _reaction_ids(db, user, "topic", "favorite"),
        _reaction_ids(db, user, "comment", "like"),
        _reaction_ids(db, user, "comment", "favorite"),
    )


def create_topic(db: Session, user: models.User, data: SquareTopicCreate) -> dict:
    title = data.title or data.content.strip().replace("\n", " ")[:24] or "广场动态"
    badge = data.badge or (data.tags[0] if data.tags else "随笔")
    topic = models.SquareTopic(
        user_id=user.id,
        title=title,
        content=data.content,
        badge=badge,
        tags=dump_json_list(data.tags or [badge]),
        images=dump_json_list(data.images),
    )
    db.add(topic)
    db.commit()
    db.refresh(topic)
    cache.clear_prefix("square:feed:")
    return get_topic(db, user, topic.id)


def toggle_reaction(db: Session, user: models.User, target_type: str, target_id: int, reaction_type: str) -> dict:
    reaction = db.scalar(
        select(models.SquareReaction).where(
            models.SquareReaction.user_id == user.id,
            models.SquareReaction.target_type == target_type,
            models.SquareReaction.target_id == target_id,
            models.SquareReaction.reaction_type == reaction_type,
        )
    )
    target = db.get(models.SquareTopic if target_type == "topic" else models.SquareComment, target_id)
    if target is None:
        raise BusinessError("目标不存在", code=40404, status_code=404)
    active = reaction is None
    count_field = "like_count" if reaction_type == "like" else "favorite_count"
    if active:
        db.add(models.SquareReaction(user_id=user.id, target_type=target_type, target_id=target_id, reaction_type=reaction_type))
        setattr(target, count_field, getattr(target, count_field) + 1)
    else:
        db.delete(reaction)
        setattr(target, count_field, max(0, getattr(target, count_field) - 1))
    db.commit()
    return {"id": target_id, "active": active}


def increase_share(db: Session, topic_id: int) -> dict:
    topic = db.get(models.SquareTopic, topic_id)
    if topic is None:
        raise BusinessError("内容不存在", code=40403, status_code=404)
    topic.share_count += 1
    db.commit()
    return {"id": topic_id, "shareCount": topic.share_count}


def create_comment(db: Session, user: models.User, topic_id: int, data: SquareCommentCreate) -> dict:
    topic = db.get(models.SquareTopic, topic_id)
    if topic is None:
        raise BusinessError("内容不存在", code=40403, status_code=404)
    comment = models.SquareComment(topic_id=topic_id, user_id=user.id, content=data.content)
    db.add(comment)
    db.commit()
    return get_topic(db, user, topic_id)


def list_my_topics(db: Session, user: models.User, page: int, page_size: int) -> dict:
    stmt = (
        select(models.SquareTopic)
        .options(selectinload(models.SquareTopic.author), selectinload(models.SquareTopic.comments))
        .where(models.SquareTopic.user_id == user.id)
        .order_by(models.SquareTopic.created_at.desc())
    )
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    items = [
        {
            "id": row.id,
            "kind": "post",
            "title": row.title,
            "subtitle": user.nickname,
            "content": row.content,
            "badge": row.badge,
            "meta": "",
            "likeCount": row.like_count,
            "favoriteCount": row.favorite_count,
            "targetUrl": f"/pages/square-detail/square-detail?id={row.id}",
        }
        for row in rows
    ]
    return page_dict(items, page, page_size, total)


def list_liked_topics(db: Session, user: models.User, page: int, page_size: int) -> dict:
    stmt = (
        select(models.SquareTopic)
        .options(selectinload(models.SquareTopic.author))
        .where(models.SquareTopic.user_id == user.id)
        .order_by(models.SquareTopic.like_count.desc(), models.SquareTopic.created_at.desc())
    )
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    items = [
        {
            "id": row.id,
            "kind": "post",
            "title": row.title,
            "subtitle": row.author.nickname if row.author else "诗词访客",
            "content": row.content,
            "badge": "获赞",
            "meta": "",
            "likeCount": row.like_count,
            "favoriteCount": row.favorite_count,
            "targetUrl": f"/pages/square-detail/square-detail?id={row.id}",
        }
        for row in rows
    ]
    return page_dict(items, page, page_size, total)
