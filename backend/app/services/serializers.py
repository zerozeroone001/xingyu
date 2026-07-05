from __future__ import annotations

from datetime import datetime
from typing import Any

from app.db import models
from app.utils.json_util import parse_json_list


def human_time(value: datetime | None) -> str:
    if value is None:
        return ""
    return value.strftime("%Y-%m-%d %H:%M")


def user_public(user: models.User | None) -> dict[str, Any]:
    if user is None:
        return {
            "id": 0,
            "nickname": "诗词访客",
            "avatar_url": "",
            "avatarText": "诗",
            "avatarTone": "green",
        }
    return {
        "id": user.id,
        "nickname": user.nickname,
        "avatar_url": user.avatar_url,
        "avatarText": user.avatar_text,
        "avatarTone": "green",
        "title": user.title,
        "level": user.level,
    }


def user_detail(user: models.User, stats: dict[str, int] | None = None) -> dict[str, Any]:
    data = user_public(user)
    data.update(
        {
            "avatar_text": user.avatar_text,
            "gender": user.gender,
            "city": user.city,
            "bio": user.bio,
            "poem_count": 0,
            "like_count": 0,
            "favorite_count": 0,
            "following_count": 0,
        }
    )
    if stats:
        data.update(stats)
    return data


def poem_item(
    poem: models.Poem,
    favorite_ids: set[int] | None = None,
    liked_ids: set[int] | None = None,
) -> dict[str, Any]:
    favorite_ids = favorite_ids or set()
    liked_ids = liked_ids or set()
    return {
        "id": poem.id,
        "title": poem.title,
        "dynasty": poem.dynasty,
        "author": poem.author,
        "content": poem.content,
        "recommend_sentence": poem.recommend_sentence,
        "tags": parse_json_list(poem.tags),
        "is_favorite": poem.id in favorite_ids,
        "is_liked": poem.id in liked_ids,
        "like_count": poem.like_count,
        "favorite_count": poem.favorite_count,
        "share_count": poem.share_count,
    }


def square_comment_item(comment: models.SquareComment, liked: bool = False, favorited: bool = False) -> dict[str, Any]:
    return {
        "id": comment.id,
        "nickname": comment.author.nickname if comment.author else "诗词访客",
        "avatarText": comment.author.avatar_text if comment.author else "诗",
        "avatarTone": "green",
        "content": comment.content,
        "time": human_time(comment.created_at),
        "likeCount": comment.like_count,
        "favoriteCount": comment.favorite_count,
        "isLiked": liked,
        "isFavorited": favorited,
    }


def square_topic_item(
    topic: models.SquareTopic,
    liked_ids: set[int] | None = None,
    favorite_ids: set[int] | None = None,
    comment_liked_ids: set[int] | None = None,
    comment_favorite_ids: set[int] | None = None,
) -> dict[str, Any]:
    liked_ids = liked_ids or set()
    favorite_ids = favorite_ids or set()
    comment_liked_ids = comment_liked_ids or set()
    comment_favorite_ids = comment_favorite_ids or set()
    return {
        "id": topic.id,
        "title": topic.title,
        "content": topic.content,
        "badge": topic.badge,
        "tags": parse_json_list(topic.tags),
        "time": human_time(topic.created_at),
        "author": user_public(topic.author),
        "images": parse_json_list(topic.images),
        "likeCount": topic.like_count,
        "favoriteCount": topic.favorite_count,
        "shareCount": topic.share_count,
        "isLiked": topic.id in liked_ids,
        "isFavorited": topic.id in favorite_ids,
        "comments": [
            square_comment_item(comment, comment.id in comment_liked_ids, comment.id in comment_favorite_ids)
            for comment in sorted(topic.comments, key=lambda item: item.created_at, reverse=True)
        ],
    }


def feihualing_record_item(record: models.FeihualingRecord) -> dict[str, Any]:
    return {
        "id": record.id,
        "keyword": record.keyword,
        "answer": record.answer,
        "is_correct": record.is_correct,
        "score": record.score,
        "created_at": record.created_at.isoformat(),
        "source": {
            "title": record.source_title,
            "author": record.source_author,
            "dynasty": record.source_dynasty,
        }
        if record.source_title
        else None,
    }


def feihualing_room_item(room: models.FeihualingRoom) -> dict[str, Any]:
    messages = sorted(room.messages, key=lambda item: item.created_at)
    latest_message = messages[-1] if messages else None
    is_playing = "第" in room.round_text
    is_ended = "结束" in room.round_text

    return {
        "id": room.id,
        "title": room.title,
        "keyword": room.keyword,
        "canWatch": room.can_watch,
        "playerCount": room.player_count,
        "maxPlayers": room.max_players,
        "roundText": room.round_text,
        "statusText": room.round_text,
        "latestLine": latest_message.content if latest_message else "等待诗友开局",
        "resultText": "已结束" if is_ended else ("进行中" if is_playing else "招募中"),
        "joinedAt": human_time(room.created_at),
        "creator": user_public(room.creator),
        "battleMessages": [
            {
                "role": message.role,
                "playerName": message.user.nickname if message.user else "诗词访客",
                "content": message.content,
                "source": {
                    "title": message.source_title,
                    "author": message.source_author,
                    "dynasty": message.source_dynasty,
                },
            }
            for message in messages
        ],
        "replyPool": [],
    }
