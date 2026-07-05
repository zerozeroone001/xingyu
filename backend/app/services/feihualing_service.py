from __future__ import annotations

from collections.abc import Iterable

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, selectinload

from app.core.cache import cache
from app.core.exceptions import BusinessError
from app.db import models
from app.schemas.feihualing import FeihualingCheckRequest, FeihualingRecordCreate, FeihualingRoomCreate
from app.services.serializers import feihualing_record_item, feihualing_room_item
from app.utils.pagination import page_dict, paginate_select


def keywords(db: Session) -> dict:
    cached = cache.get("feihualing:keywords")
    if cached is not None:
        return cached

    data = {"items": ["花", "月", "山", "水", "春", "秋", "风", "雪", "人", "江"]}
    cache.set("feihualing:keywords", data, ttl=1800)
    return data


PUNCTUATION = set(" \t\r\n，。！？、；：“”‘’《》（）,.!?;:'\"()[]{}-")
KNOWN_LINE_CORRECTIONS = {
    "床前看月光": "床前明月光",
    "举头望山月": "举头望明月",
}


def normalize_sentence(value: str) -> str:
    return "".join(char for char in value if char not in PUNCTUATION).strip()


def apply_known_corrections(value: str) -> str:
    corrected = value
    for wrong, right in KNOWN_LINE_CORRECTIONS.items():
        corrected = corrected.replace(wrong, right)
    return corrected


def normalize_with_index(value: str) -> tuple[str, list[int]]:
    chars: list[str] = []
    index_map: list[int] = []
    for index, char in enumerate(value):
        if char in PUNCTUATION:
            continue
        chars.append(char)
        index_map.append(index)
    return "".join(chars), index_map


def poem_source(poem: models.Poem | None) -> dict | None:
    if poem is None:
        return None
    return {
        "id": poem.id,
        "title": poem.title,
        "author": poem.author,
        "dynasty": poem.dynasty,
        "content": apply_known_corrections(poem.content),
    }


def iter_poem_texts(poem: models.Poem) -> Iterable[str]:
    for value in (poem.content, poem.recommend_sentence):
        if value:
            yield value
            corrected = apply_known_corrections(value)
            if corrected != value:
                yield corrected


def find_exact_canonical_match(db: Session, normalized_answer: str) -> models.Poem | None:
    if not normalized_answer:
        return None

    poems = db.scalars(select(models.Poem)).all()
    for poem in poems:
        for text in iter_poem_texts(poem):
            if normalized_answer in normalize_sentence(text):
                return poem
    return None


def typo_corrections(answer: str, candidate: str, index_map: list[int]) -> list[dict]:
    if len(answer) != len(candidate):
        return []

    corrections: list[dict] = []
    for index, char in enumerate(answer):
        if candidate[index] == char:
            continue
        corrections.append(
            {
                "index": index_map[index],
                "original": char,
                "corrected": candidate[index],
            }
        )
    return corrections


def max_allowed_typos(length: int) -> int:
    if length <= 4:
        return 1
    if length <= 14:
        return 2
    return 3


def find_best_fuzzy_match(db: Session, normalized_answer: str, index_map: list[int]) -> dict | None:
    if len(normalized_answer) < 4:
        return None

    answer_len = len(normalized_answer)
    allowed_typos = max_allowed_typos(answer_len)
    best: dict | None = None

    poems = db.scalars(select(models.Poem)).all()
    for poem in poems:
        for text in iter_poem_texts(poem):
            normalized_text = normalize_sentence(text)
            if len(normalized_text) < answer_len:
                continue

            for start in range(0, len(normalized_text) - answer_len + 1):
                candidate = normalized_text[start : start + answer_len]
                distance = sum(1 for left, right in zip(normalized_answer, candidate) if left != right)
                if distance == 0 or distance > allowed_typos:
                    continue
                if best is None or distance < best["typo_count"]:
                    corrections = typo_corrections(normalized_answer, candidate, index_map)
                    best = {
                        "poem": poem,
                        "corrected_answer": candidate,
                        "typo_count": distance,
                        "wrong_indices": [item["index"] for item in corrections],
                        "corrections": corrections,
                    }
                    if distance == 1:
                        return best

    return best


def check_answer(db: Session, data: FeihualingCheckRequest) -> dict:
    answer = data.answer.strip()
    normalized_answer, index_map = normalize_with_index(answer)
    contains_keyword = data.keyword in answer

    poem = None
    if normalized_answer:
        like = f"%{answer}%"
        poem = db.scalar(
            select(models.Poem)
            .where(or_(models.Poem.content.like(like), models.Poem.recommend_sentence.like(like)))
            .limit(1)
        )

    if poem is None and normalized_answer:
        normalized_like = f"%{normalized_answer}%"
        poem = db.scalar(
            select(models.Poem)
            .where(
                or_(
                    models.Poem.content.like(normalized_like),
                    models.Poem.recommend_sentence.like(normalized_like),
                )
            )
            .limit(1)
        )
    if poem is None and normalized_answer:
        poem = find_exact_canonical_match(db, normalized_answer)

    fuzzy_match = None if poem is not None else find_best_fuzzy_match(db, normalized_answer, index_map)
    source_poem = poem or (fuzzy_match["poem"] if fuzzy_match else None)
    typo_count = fuzzy_match["typo_count"] if fuzzy_match else 0
    is_correct = contains_keyword and poem is not None
    return {
        "keyword": data.keyword,
        "answer": answer,
        "is_correct": is_correct,
        "score": 10 if (is_correct or fuzzy_match) else 0,
        "source": poem_source(source_poem),
        "recognized": bool(poem or fuzzy_match),
        "recognition_status": "exact" if is_correct else ("typo" if fuzzy_match else "not_found"),
        "corrected_answer": fuzzy_match["corrected_answer"] if fuzzy_match else answer,
        "typo_count": typo_count,
        "wrong_indices": fuzzy_match["wrong_indices"] if fuzzy_match else [],
        "corrections": fuzzy_match["corrections"] if fuzzy_match else [],
    }


def save_record(db: Session, user: models.User, data: FeihualingRecordCreate) -> dict:
    source = data.source or {}
    record = models.FeihualingRecord(
        user_id=user.id,
        keyword=data.keyword,
        answer=data.answer,
        is_correct=data.is_correct,
        score=data.score,
        source_title=source.get("title", ""),
        source_author=source.get("author", ""),
        source_dynasty=source.get("dynasty", ""),
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return feihualing_record_item(record)


def list_records(db: Session, user: models.User, page: int, page_size: int) -> dict:
    stmt = (
        select(models.FeihualingRecord)
        .where(models.FeihualingRecord.user_id == user.id)
        .order_by(models.FeihualingRecord.created_at.desc())
    )
    rows, page, page_size, total = paginate_select(db, stmt, page, page_size)
    return page_dict([feihualing_record_item(row) for row in rows], page, page_size, total)


def list_rooms(db: Session) -> dict:
    rooms = db.scalars(
        select(models.FeihualingRoom)
        .options(
            selectinload(models.FeihualingRoom.creator),
            selectinload(models.FeihualingRoom.messages).selectinload(models.FeihualingRoomMessage.user),
        )
        .order_by(models.FeihualingRoom.created_at.desc())
    ).all()
    return {"items": [feihualing_room_item(room) for room in rooms], "online_count": max(1, len(rooms) * 3)}


def get_room(db: Session, room_id: int) -> dict:
    room = db.scalar(
        select(models.FeihualingRoom)
        .options(
            selectinload(models.FeihualingRoom.creator),
            selectinload(models.FeihualingRoom.messages).selectinload(models.FeihualingRoomMessage.user),
        )
        .where(models.FeihualingRoom.id == room_id)
    )
    if room is None:
        raise BusinessError("房间不存在", code=40405, status_code=404)
    return feihualing_room_item(room)


def create_room(db: Session, user: models.User, data: FeihualingRoomCreate) -> dict:
    can_watch = data.can_watch if data.can_watch is not None else data.canWatch
    max_players = data.max_players if data.max_players is not None else data.maxPlayers
    room = models.FeihualingRoom(
        creator_id=user.id,
        title=data.title or f"{data.keyword}字雅集",
        keyword=data.keyword,
        can_watch=True if can_watch is None else bool(can_watch),
        max_players=max_players or 4,
        round_text="招募中",
    )
    db.add(room)
    db.commit()
    db.refresh(room)
    return get_room(db, room.id)
