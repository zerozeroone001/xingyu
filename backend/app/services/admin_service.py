from __future__ import annotations

from collections import Counter
from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import delete, func, or_, select
from sqlalchemy.orm import Session, selectinload

from app.core.cache import cache
from app.core.exceptions import BusinessError
from app.db import models
from app.schemas.admin import (
    CategoryAdminPayload,
    FeihualingRoomAdminPayload,
    FeedbackAdminPayload,
    PoemAdminPayload,
    SquareTopicAdminPayload,
    UserAdminPayload,
)
from app.utils.json_util import dump_json_list, parse_json_list
from app.utils.pagination import clamp_page, clamp_page_size, page_dict, paginate_select


def _time(value: datetime | None) -> str:
    return value.strftime("%Y-%m-%d %H:%M:%S") if value else ""


def _poem_category_ids(db: Session, poem_id: int) -> list[int]:
    return list(db.scalars(select(models.PoemCategory.category_id).where(models.PoemCategory.poem_id == poem_id)).all())


def _set_poem_categories(db: Session, poem_id: int, category_ids: list[int]) -> None:
    db.execute(delete(models.PoemCategory).where(models.PoemCategory.poem_id == poem_id))
    for category_id in sorted(set(category_ids)):
        if db.get(models.Category, category_id) is not None:
            db.add(models.PoemCategory(poem_id=poem_id, category_id=category_id))


def _ensure_poem_name(db: Session, title: str) -> None:
    if not db.scalar(select(models.PoemName).where(models.PoemName.name == title)):
        db.add(models.PoemName(name=title))


def _prune_orphan_poem_names(db: Session) -> None:
    poem_titles = set(db.scalars(select(models.Poem.title)).all())
    for poem_name in db.scalars(select(models.PoemName)).all():
        if poem_name.name not in poem_titles:
            db.delete(poem_name)


def poem_row(db: Session, poem: models.Poem) -> dict[str, Any]:
    return {
        "id": poem.id,
        "title": poem.title,
        "dynasty": poem.dynasty,
        "author": poem.author,
        "content": poem.content,
        "recommend_sentence": poem.recommend_sentence,
        "tags": parse_json_list(poem.tags),
        "category_ids": _poem_category_ids(db, poem.id),
        "like_count": poem.like_count,
        "favorite_count": poem.favorite_count,
        "share_count": poem.share_count,
        "created_at": _time(poem.created_at),
        "updated_at": _time(poem.updated_at),
    }


def category_row(category: models.Category, poem_count: int = 0) -> dict[str, Any]:
    return {
        "id": category.id,
        "name": category.name,
        "type": category.type,
        "sort_order": category.sort_order,
        "poem_count": poem_count,
    }


def user_row(db: Session, user: models.User) -> dict[str, Any]:
    return {
        "id": user.id,
        "openid": user.openid,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "avatar_text": user.avatar_text,
        "title": user.title,
        "level": user.level,
        "gender": user.gender,
        "city": user.city,
        "bio": user.bio,
        "favorite_count": db.scalar(select(func.count()).select_from(models.Favorite).where(models.Favorite.user_id == user.id)) or 0,
        "topic_count": db.scalar(select(func.count()).select_from(models.SquareTopic).where(models.SquareTopic.user_id == user.id)) or 0,
        "created_at": _time(user.created_at),
        "updated_at": _time(user.updated_at),
    }


def topic_row(topic: models.SquareTopic) -> dict[str, Any]:
    return {
        "id": topic.id,
        "user_id": topic.user_id,
        "author": topic.author.nickname if topic.author else "",
        "title": topic.title,
        "content": topic.content,
        "badge": topic.badge,
        "tags": parse_json_list(topic.tags),
        "images": parse_json_list(topic.images),
        "like_count": topic.like_count,
        "favorite_count": topic.favorite_count,
        "share_count": topic.share_count,
        "comment_count": len(topic.comments),
        "created_at": _time(topic.created_at),
        "updated_at": _time(topic.updated_at),
    }


def comment_row(comment: models.SquareComment) -> dict[str, Any]:
    return {
        "id": comment.id,
        "topic_id": comment.topic_id,
        "user_id": comment.user_id,
        "author": comment.author.nickname if comment.author else "",
        "content": comment.content,
        "like_count": comment.like_count,
        "favorite_count": comment.favorite_count,
        "created_at": _time(comment.created_at),
        "updated_at": _time(comment.updated_at),
    }


def feedback_row(item: models.Feedback) -> dict[str, Any]:
    return {
        "id": item.id,
        "user_id": item.user_id,
        "content": item.content,
        "contact": item.contact,
        "status": item.status,
        "created_at": _time(item.created_at),
    }


def room_row(room: models.FeihualingRoom) -> dict[str, Any]:
    return {
        "id": room.id,
        "creator_id": room.creator_id,
        "creator": room.creator.nickname if room.creator else "",
        "title": room.title,
        "keyword": room.keyword,
        "can_watch": room.can_watch,
        "player_count": room.player_count,
        "max_players": room.max_players,
        "round_text": room.round_text,
        "message_count": len(room.messages),
        "created_at": _time(room.created_at),
        "updated_at": _time(room.updated_at),
    }


def record_row(record: models.FeihualingRecord) -> dict[str, Any]:
    return {
        "id": record.id,
        "user_id": record.user_id,
        "keyword": record.keyword,
        "answer": record.answer,
        "is_correct": record.is_correct,
        "score": record.score,
        "source_title": record.source_title,
        "source_author": record.source_author,
        "source_dynasty": record.source_dynasty,
        "created_at": _time(record.created_at),
    }


def dashboard(db: Session) -> dict[str, Any]:
    counts = {
        "poems": db.scalar(select(func.count()).select_from(models.Poem)) or 0,
        "categories": db.scalar(select(func.count()).select_from(models.Category)) or 0,
        "users": db.scalar(select(func.count()).select_from(models.User)) or 0,
        "topics": db.scalar(select(func.count()).select_from(models.SquareTopic)) or 0,
        "comments": db.scalar(select(func.count()).select_from(models.SquareComment)) or 0,
        "feedback": db.scalar(select(func.count()).select_from(models.Feedback)) or 0,
        "rooms": db.scalar(select(func.count()).select_from(models.FeihualingRoom)) or 0,
        "records": db.scalar(select(func.count()).select_from(models.FeihualingRecord)) or 0,
    }
    hot_poems = db.scalars(
        select(models.Poem).order_by(models.Poem.like_count.desc(), models.Poem.favorite_count.desc(), models.Poem.id.asc()).limit(8)
    ).all()
    latest_topics = db.scalars(
        select(models.SquareTopic)
        .options(selectinload(models.SquareTopic.author), selectinload(models.SquareTopic.comments))
        .order_by(models.SquareTopic.created_at.desc())
        .limit(6)
    ).all()
    feedback_status = Counter(db.scalars(select(models.Feedback.status)).all())
    today = datetime.utcnow().date()
    trend = []
    for offset in range(6, -1, -1):
        day = today - timedelta(days=offset)
        start = datetime.combine(day, datetime.min.time())
        end = start + timedelta(days=1)
        trend.append(
            {
                "date": day.strftime("%m-%d"),
                "users": db.scalar(select(func.count()).select_from(models.User).where(models.User.created_at >= start, models.User.created_at < end)) or 0,
                "topics": db.scalar(
                    select(func.count()).select_from(models.SquareTopic).where(models.SquareTopic.created_at >= start, models.SquareTopic.created_at < end)
                )
                or 0,
                "feedback": db.scalar(select(func.count()).select_from(models.Feedback).where(models.Feedback.created_at >= start, models.Feedback.created_at < end))
                or 0,
            }
        )
    return {
        "counts": counts,
        "hot_poems": [poem_row(db, item) for item in hot_poems],
        "latest_topics": [topic_row(item) for item in latest_topics],
        "feedback_status": dict(feedback_status),
        "trend": trend,
    }


def list_poems(db: Session, page: int, page_size: int, keyword: str = "", dynasty: str = "", author: str = "") -> dict[str, Any]:
    stmt = select(models.Poem).order_by(models.Poem.updated_at.desc(), models.Poem.id.desc())
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(or_(models.Poem.title.like(like), models.Poem.content.like(like), models.Poem.recommend_sentence.like(like)))
    if dynasty:
        stmt = stmt.where(models.Poem.dynasty == dynasty)
    if author:
        stmt = stmt.where(models.Poem.author.like(f"%{author}%"))
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    return page_dict([poem_row(db, row) for row in rows], page, page_size, total)


def create_poem(db: Session, payload: PoemAdminPayload) -> dict[str, Any]:
    poem = models.Poem(
        title=payload.title,
        dynasty=payload.dynasty,
        author=payload.author,
        content=payload.content,
        recommend_sentence=payload.recommend_sentence,
        tags=dump_json_list(payload.tags),
        like_count=payload.like_count,
        favorite_count=payload.favorite_count,
        share_count=payload.share_count,
    )
    db.add(poem)
    db.flush()
    _set_poem_categories(db, poem.id, payload.category_ids)
    _ensure_poem_name(db, payload.title)
    db.commit()
    db.refresh(poem)
    cache.clear_prefix("home:data:")
    cache.clear_prefix("category:")
    return poem_row(db, poem)


def update_poem(db: Session, poem_id: int, payload: PoemAdminPayload) -> dict[str, Any]:
    poem = db.get(models.Poem, poem_id)
    if poem is None:
        raise BusinessError("Poem not found", code=40401, status_code=404)
    old_title = poem.title
    poem.title = payload.title
    poem.dynasty = payload.dynasty
    poem.author = payload.author
    poem.content = payload.content
    poem.recommend_sentence = payload.recommend_sentence
    poem.tags = dump_json_list(payload.tags)
    poem.like_count = payload.like_count
    poem.favorite_count = payload.favorite_count
    poem.share_count = payload.share_count
    _set_poem_categories(db, poem.id, payload.category_ids)
    _ensure_poem_name(db, payload.title)
    if old_title != payload.title:
        db.flush()
        _prune_orphan_poem_names(db)
    db.commit()
    db.refresh(poem)
    cache.clear_prefix("poem:detail:")
    cache.clear_prefix("home:data:")
    cache.clear_prefix("category:")
    return poem_row(db, poem)


def delete_poem(db: Session, poem_id: int) -> dict[str, Any]:
    poem = db.get(models.Poem, poem_id)
    if poem is None:
        raise BusinessError("Poem not found", code=40401, status_code=404)
    db.execute(delete(models.PoemCategory).where(models.PoemCategory.poem_id == poem_id))
    db.execute(delete(models.Favorite).where(models.Favorite.poem_id == poem_id))
    db.execute(delete(models.BrowseHistory).where(models.BrowseHistory.poem_id == poem_id))
    db.execute(delete(models.SquareReaction).where(models.SquareReaction.target_type == "poem", models.SquareReaction.target_id == poem_id))
    db.delete(poem)
    db.flush()
    _prune_orphan_poem_names(db)
    db.commit()
    cache.clear_prefix("poem:detail:")
    cache.clear_prefix("home:data:")
    cache.clear_prefix("category:")
    return {"deleted": True, "id": poem_id}


def list_categories(db: Session) -> dict[str, Any]:
    poem_count = func.count(models.PoemCategory.poem_id).label("poem_count")
    rows = db.execute(
        select(models.Category, poem_count)
        .outerjoin(models.PoemCategory, models.PoemCategory.category_id == models.Category.id)
        .group_by(models.Category.id)
        .order_by(models.Category.sort_order.asc(), models.Category.id.asc())
    ).all()
    return {"items": [category_row(category, count or 0) for category, count in rows]}


def create_category(db: Session, payload: CategoryAdminPayload) -> dict[str, Any]:
    category = models.Category(name=payload.name, type=payload.type, sort_order=payload.sort_order)
    db.add(category)
    db.commit()
    db.refresh(category)
    cache.clear_prefix("category:")
    return category_row(category)


def update_category(db: Session, category_id: int, payload: CategoryAdminPayload) -> dict[str, Any]:
    category = db.get(models.Category, category_id)
    if category is None:
        raise BusinessError("Category not found", code=40402, status_code=404)
    category.name = payload.name
    category.type = payload.type
    category.sort_order = payload.sort_order
    db.commit()
    cache.clear_prefix("category:")
    return category_row(category)


def delete_category(db: Session, category_id: int) -> dict[str, Any]:
    category = db.get(models.Category, category_id)
    if category is None:
        raise BusinessError("Category not found", code=40402, status_code=404)
    db.execute(delete(models.PoemCategory).where(models.PoemCategory.category_id == category_id))
    db.delete(category)
    db.commit()
    cache.clear_prefix("category:")
    return {"deleted": True, "id": category_id}


def list_users(db: Session, page: int, page_size: int, keyword: str = "") -> dict[str, Any]:
    stmt = select(models.User).order_by(models.User.created_at.desc(), models.User.id.desc())
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(or_(models.User.nickname.like(like), models.User.openid.like(like), models.User.city.like(like)))
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    return page_dict([user_row(db, row) for row in rows], page, page_size, total)


def update_user(db: Session, user_id: int, payload: UserAdminPayload) -> dict[str, Any]:
    user = db.get(models.User, user_id)
    if user is None:
        raise BusinessError("User not found", code=40403, status_code=404)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user_row(db, user)


def list_topics(db: Session, page: int, page_size: int, keyword: str = "", user_id: int | None = None) -> dict[str, Any]:
    stmt = (
        select(models.SquareTopic)
        .options(selectinload(models.SquareTopic.author), selectinload(models.SquareTopic.comments))
        .order_by(models.SquareTopic.created_at.desc(), models.SquareTopic.id.desc())
    )
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(or_(models.SquareTopic.title.like(like), models.SquareTopic.content.like(like), models.SquareTopic.badge.like(like)))
    if user_id:
        stmt = stmt.where(models.SquareTopic.user_id == user_id)
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    return page_dict([topic_row(row) for row in rows], page, page_size, total)


def update_topic(db: Session, topic_id: int, payload: SquareTopicAdminPayload) -> dict[str, Any]:
    topic = db.get(models.SquareTopic, topic_id)
    if topic is None:
        raise BusinessError("Topic not found", code=40404, status_code=404)
    data = payload.model_dump(exclude_unset=True)
    for field in ("title", "content", "badge"):
        if data.get(field) is not None:
            setattr(topic, field, data[field])
    if data.get("tags") is not None:
        topic.tags = dump_json_list(data["tags"])
    if data.get("images") is not None:
        topic.images = dump_json_list(data["images"])
    db.commit()
    topic = db.scalar(
        select(models.SquareTopic)
        .options(selectinload(models.SquareTopic.author), selectinload(models.SquareTopic.comments))
        .where(models.SquareTopic.id == topic_id)
    )
    return topic_row(topic)


def delete_topic(db: Session, topic_id: int) -> dict[str, Any]:
    topic = db.get(models.SquareTopic, topic_id)
    if topic is None:
        raise BusinessError("Topic not found", code=40404, status_code=404)
    comment_ids = list(db.scalars(select(models.SquareComment.id).where(models.SquareComment.topic_id == topic_id)).all())
    if comment_ids:
        db.execute(delete(models.SquareReaction).where(models.SquareReaction.target_type == "comment", models.SquareReaction.target_id.in_(comment_ids)))
    db.execute(delete(models.SquareReaction).where(models.SquareReaction.target_type == "topic", models.SquareReaction.target_id == topic_id))
    db.delete(topic)
    db.commit()
    return {"deleted": True, "id": topic_id}


def list_comments(db: Session, page: int, page_size: int, keyword: str = "", topic_id: int | None = None) -> dict[str, Any]:
    stmt = (
        select(models.SquareComment)
        .options(selectinload(models.SquareComment.author))
        .order_by(models.SquareComment.created_at.desc(), models.SquareComment.id.desc())
    )
    if keyword:
        stmt = stmt.where(models.SquareComment.content.like(f"%{keyword}%"))
    if topic_id:
        stmt = stmt.where(models.SquareComment.topic_id == topic_id)
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    return page_dict([comment_row(row) for row in rows], page, page_size, total)


def delete_comment(db: Session, comment_id: int) -> dict[str, Any]:
    comment = db.get(models.SquareComment, comment_id)
    if comment is None:
        raise BusinessError("Comment not found", code=40405, status_code=404)
    db.execute(delete(models.SquareReaction).where(models.SquareReaction.target_type == "comment", models.SquareReaction.target_id == comment_id))
    db.delete(comment)
    db.commit()
    return {"deleted": True, "id": comment_id}


def list_feedback(db: Session, page: int, page_size: int, status: str = "") -> dict[str, Any]:
    stmt = select(models.Feedback).order_by(models.Feedback.created_at.desc(), models.Feedback.id.desc())
    if status:
        stmt = stmt.where(models.Feedback.status == status)
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    return page_dict([feedback_row(row) for row in rows], page, page_size, total)


def update_feedback(db: Session, feedback_id: int, payload: FeedbackAdminPayload) -> dict[str, Any]:
    item = db.get(models.Feedback, feedback_id)
    if item is None:
        raise BusinessError("Feedback not found", code=40406, status_code=404)
    item.status = payload.status
    db.commit()
    return feedback_row(item)


def delete_feedback(db: Session, feedback_id: int) -> dict[str, Any]:
    item = db.get(models.Feedback, feedback_id)
    if item is None:
        raise BusinessError("Feedback not found", code=40406, status_code=404)
    db.delete(item)
    db.commit()
    return {"deleted": True, "id": feedback_id}


def list_rooms(db: Session, page: int, page_size: int, keyword: str = "") -> dict[str, Any]:
    stmt = (
        select(models.FeihualingRoom)
        .options(selectinload(models.FeihualingRoom.creator), selectinload(models.FeihualingRoom.messages))
        .order_by(models.FeihualingRoom.created_at.desc(), models.FeihualingRoom.id.desc())
    )
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(or_(models.FeihualingRoom.title.like(like), models.FeihualingRoom.keyword.like(like), models.FeihualingRoom.round_text.like(like)))
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    return page_dict([room_row(row) for row in rows], page, page_size, total)


def update_room(db: Session, room_id: int, payload: FeihualingRoomAdminPayload) -> dict[str, Any]:
    room = db.get(models.FeihualingRoom, room_id)
    if room is None:
        raise BusinessError("Room not found", code=40407, status_code=404)
    for field, value in payload.model_dump(exclude_unset=True).items():
        if value is not None:
            setattr(room, field, value)
    db.commit()
    room = db.scalar(
        select(models.FeihualingRoom)
        .options(selectinload(models.FeihualingRoom.creator), selectinload(models.FeihualingRoom.messages))
        .where(models.FeihualingRoom.id == room_id)
    )
    return room_row(room)


def delete_room(db: Session, room_id: int) -> dict[str, Any]:
    room = db.get(models.FeihualingRoom, room_id)
    if room is None:
        raise BusinessError("Room not found", code=40407, status_code=404)
    db.delete(room)
    db.commit()
    return {"deleted": True, "id": room_id}


def list_records(db: Session, page: int, page_size: int, keyword: str = "") -> dict[str, Any]:
    page = clamp_page(page)
    page_size = clamp_page_size(page_size)
    stmt = select(models.FeihualingRecord).order_by(models.FeihualingRecord.created_at.desc(), models.FeihualingRecord.id.desc())
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(or_(models.FeihualingRecord.keyword.like(like), models.FeihualingRecord.answer.like(like)))
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    return page_dict([record_row(row) for row in rows], page, page_size, total)
