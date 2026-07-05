from __future__ import annotations

from sqlalchemy import func, or_, select
from sqlalchemy.orm import Session

from app.core.cache import cache
from app.core.exceptions import BusinessError
from app.db import models
from app.services.serializers import poem_item
from app.utils.pagination import clamp_page, clamp_page_size, page_dict, paginate_select


def poem_hot_order() -> tuple:
    return (
        models.Poem.like_count.desc(),
        models.Poem.favorite_count.desc(),
        models.Poem.share_count.desc(),
        models.Poem.id.asc(),
    )


def favorite_ids_for_user(db: Session, user: models.User | None) -> set[int]:
    if user is None:
        return set()
    return set(db.scalars(select(models.Favorite.poem_id).where(models.Favorite.user_id == user.id)).all())


def liked_ids_for_user(db: Session, user: models.User | None) -> set[int]:
    if user is None:
        return set()
    return set(
        db.scalars(
            select(models.SquareReaction.target_id).where(
                models.SquareReaction.user_id == user.id,
                models.SquareReaction.target_type == "poem",
                models.SquareReaction.reaction_type == "like",
            )
        ).all()
    )


def poem_counts(poem: models.Poem, favorite_ids: set[int] | None = None, liked_ids: set[int] | None = None) -> dict:
    favorite_ids = favorite_ids or set()
    liked_ids = liked_ids or set()
    return {
        "poem_id": poem.id,
        "id": poem.id,
        "is_liked": poem.id in liked_ids,
        "is_favorite": poem.id in favorite_ids,
        "like_count": poem.like_count,
        "favorite_count": poem.favorite_count,
        "share_count": poem.share_count,
    }


def list_poems(db: Session, user: models.User | None, page: int = 1, page_size: int = 10, keyword: str | None = None) -> dict:
    stmt = select(models.Poem).order_by(*poem_hot_order())
    if keyword:
        like = f"%{keyword}%"
        stmt = stmt.where(or_(models.Poem.title.like(like), models.Poem.author.like(like), models.Poem.content.like(like)))
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    favorite_ids = favorite_ids_for_user(db, user)
    liked_ids = liked_ids_for_user(db, user)
    return page_dict([poem_item(row, favorite_ids, liked_ids) for row in rows], page, page_size, total)


def get_poem_detail(db: Session, poem_id: int, user: models.User | None) -> dict:
    key = f"poem:detail:{poem_id}:{user.id if user else 0}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    poem = db.get(models.Poem, poem_id)
    if poem is None:
        raise BusinessError("诗词不存在", code=40401, status_code=404)
    favorite_ids = favorite_ids_for_user(db, user)
    liked_ids = liked_ids_for_user(db, user)
    data = poem_item(poem, favorite_ids, liked_ids)
    data["related_poems"] = [
        poem_item(item, favorite_ids, liked_ids)
        for item in db.scalars(
            select(models.Poem).where(models.Poem.id != poem_id, models.Poem.author == poem.author).order_by(*poem_hot_order()).limit(3)
        ).all()
    ]
    cache.set(key, data, ttl=1800)
    return data


def home_data(db: Session, user: models.User | None) -> dict:
    key = f"home:data:{user.id if user else 0}"
    cached = cache.get(key)
    if cached is not None:
        return cached
    poems = db.scalars(select(models.Poem).order_by(*poem_hot_order()).limit(10)).all()
    favorite_ids = favorite_ids_for_user(db, user)
    liked_ids = liked_ids_for_user(db, user)
    categories = db.scalars(select(models.Category).order_by(models.Category.sort_order.asc()).limit(8)).all()
    data = {
        "banners": [{"id": 1, "title": "今日诗意", "poem_id": poems[0].id if poems else 0}],
        "today_poem": poem_item(poems[0], favorite_ids, liked_ids) if poems else None,
        "recommend_poems": [poem_item(poem, favorite_ids, liked_ids) for poem in poems],
        "categories": [{"id": item.id, "name": item.name, "type": item.type} for item in categories],
        "hot_keywords": ["花", "月", "山", "水", "春", "秋"],
    }
    cache.set(key, data, ttl=300)
    return data


def list_categories(db: Session) -> dict:
    cached = cache.get("category:list")
    if cached is not None:
        return cached
    poem_count = func.count(models.PoemCategory.poem_id).label("poem_count")
    rows = db.execute(
        select(models.Category, poem_count)
        .outerjoin(models.PoemCategory, models.PoemCategory.category_id == models.Category.id)
        .group_by(models.Category.id, models.Category.name, models.Category.type, models.Category.sort_order)
        .order_by(models.Category.sort_order.asc(), models.Category.id.asc())
    ).all()
    items = [
        {
            "id": category.id,
            "name": category.name,
            "type": category.type,
            "sort_order": category.sort_order,
            "poem_count": count,
            "poemCount": count,
        }
        for category, count in rows
    ]
    data = {"items": items}
    cache.set("category:list", data, ttl=1800)
    return data


def list_category_poems(db: Session, category_id: int, user: models.User | None, page: int, page_size: int) -> dict:
    page = clamp_page(page)
    page_size = clamp_page_size(page_size)
    category = db.get(models.Category, category_id)
    if category is None:
        raise BusinessError("分类不存在", code=40402, status_code=404)
    poem_ids = select(models.PoemCategory.poem_id).where(models.PoemCategory.category_id == category_id)
    stmt = select(models.Poem).where(models.Poem.id.in_(poem_ids)).order_by(*poem_hot_order())
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    favorite_ids = favorite_ids_for_user(db, user)
    liked_ids = liked_ids_for_user(db, user)
    return page_dict([poem_item(row, favorite_ids, liked_ids) for row in rows], page, page_size, total)


def add_favorite(db: Session, user: models.User, poem_id: int) -> dict:
    poem = db.get(models.Poem, poem_id)
    if poem is None:
        raise BusinessError("诗词不存在", code=40401, status_code=404)
    exists = db.scalar(select(models.Favorite).where(models.Favorite.user_id == user.id, models.Favorite.poem_id == poem_id))
    if exists is None:
        db.add(models.Favorite(user_id=user.id, poem_id=poem_id))
        poem.favorite_count += 1
        db.commit()
        cache.clear_prefix("poem:detail:")
        cache.clear_prefix("home:data:")
    else:
        db.refresh(poem)
    return poem_counts(poem, {poem_id}, liked_ids_for_user(db, user))


def remove_favorite(db: Session, user: models.User, poem_id: int) -> dict:
    favorite = db.scalar(select(models.Favorite).where(models.Favorite.user_id == user.id, models.Favorite.poem_id == poem_id))
    if favorite is not None:
        poem = db.get(models.Poem, poem_id)
        db.delete(favorite)
        if poem is not None:
            poem.favorite_count = max(0, poem.favorite_count - 1)
        db.commit()
        cache.clear_prefix("poem:detail:")
        cache.clear_prefix("home:data:")
    poem = db.get(models.Poem, poem_id)
    if poem is None:
        raise BusinessError("诗词不存在", code=40401, status_code=404)
    return poem_counts(poem, set(), liked_ids_for_user(db, user))


def set_like(db: Session, user: models.User, poem_id: int, active: bool) -> dict:
    poem = db.get(models.Poem, poem_id)
    if poem is None:
        raise BusinessError("诗词不存在", code=40401, status_code=404)
    reaction = db.scalar(
        select(models.SquareReaction).where(
            models.SquareReaction.user_id == user.id,
            models.SquareReaction.target_type == "poem",
            models.SquareReaction.target_id == poem_id,
            models.SquareReaction.reaction_type == "like",
        )
    )

    if active and reaction is None:
        db.add(models.SquareReaction(user_id=user.id, target_type="poem", target_id=poem_id, reaction_type="like"))
        poem.like_count += 1
        db.commit()
        cache.clear_prefix("poem:detail:")
        cache.clear_prefix("home:data:")
    elif not active and reaction is not None:
        db.delete(reaction)
        poem.like_count = max(0, poem.like_count - 1)
        db.commit()
        cache.clear_prefix("poem:detail:")
        cache.clear_prefix("home:data:")
    else:
        db.refresh(poem)

    return poem_counts(poem, favorite_ids_for_user(db, user), {poem_id} if active else set())


def increase_share(db: Session, poem_id: int) -> dict:
    poem = db.get(models.Poem, poem_id)
    if poem is None:
        raise BusinessError("诗词不存在", code=40401, status_code=404)
    poem.share_count += 1
    db.commit()
    cache.clear_prefix("poem:detail:")
    cache.clear_prefix("home:data:")
    return poem_counts(poem)


def list_favorites(db: Session, user: models.User, page: int, page_size: int) -> dict:
    stmt = select(models.Favorite).where(models.Favorite.user_id == user.id).order_by(models.Favorite.created_at.desc())
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    liked_ids = liked_ids_for_user(db, user)
    items = [poem_item(row.poem, {row.poem_id}, liked_ids) for row in rows if row.poem is not None]
    return page_dict(items, page, page_size, total)


def record_history(db: Session, user: models.User, poem_id: int) -> dict:
    poem = db.get(models.Poem, poem_id)
    if poem is None:
        raise BusinessError("诗词不存在", code=40401, status_code=404)
    history = db.scalar(select(models.BrowseHistory).where(models.BrowseHistory.user_id == user.id, models.BrowseHistory.poem_id == poem_id))
    if history is None:
        db.add(models.BrowseHistory(user_id=user.id, poem_id=poem_id))
    else:
        history.viewed_at = models.now()
    db.commit()
    return {"poem_id": poem_id, "recorded": True}


def list_history(db: Session, user: models.User, page: int, page_size: int) -> dict:
    stmt = select(models.BrowseHistory).where(models.BrowseHistory.user_id == user.id).order_by(models.BrowseHistory.viewed_at.desc())
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    favorite_ids = favorite_ids_for_user(db, user)
    liked_ids = liked_ids_for_user(db, user)
    items = [poem_item(row.poem, favorite_ids, liked_ids) for row in rows if row.poem is not None]
    return page_dict(items, page, page_size, total)
