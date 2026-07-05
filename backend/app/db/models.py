from __future__ import annotations

from datetime import datetime

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


def now() -> datetime:
    return datetime.utcnow()


class TimestampMixin:
    created_at = Column(DateTime, default=now, nullable=False)
    updated_at = Column(DateTime, default=now, onupdate=now, nullable=False)


class User(Base, TimestampMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    openid = Column(String(128), unique=True, index=True, nullable=False)
    nickname = Column(String(80), default="诗词访客", nullable=False)
    avatar_url = Column(String(500), default="", nullable=False)
    avatar_text = Column(String(8), default="诗", nullable=False)
    title = Column(String(80), default="翰林学士", nullable=False)
    level = Column(Integer, default=1, nullable=False)
    gender = Column(String(20), default="保密", nullable=False)
    city = Column(String(80), default="", nullable=False)
    bio = Column(Text, default="", nullable=False)


class Poem(Base, TimestampMixin):
    __tablename__ = "poems"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), index=True, nullable=False)
    dynasty = Column(String(40), index=True, nullable=False)
    author = Column(String(80), index=True, nullable=False)
    content = Column(Text, nullable=False)
    recommend_sentence = Column(Text, default="", nullable=False)
    tags = Column(Text, default="[]", nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    favorite_count = Column(Integer, default=0, nullable=False)
    share_count = Column(Integer, default=0, nullable=False)


class PoemName(Base):
    __tablename__ = "poem_names"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), index=True, nullable=False)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(80), index=True, nullable=False)
    type = Column(String(40), index=True, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)


class PoemCategory(Base):
    __tablename__ = "poem_categories"
    __table_args__ = (UniqueConstraint("poem_id", "category_id", name="uq_poem_category"),)

    id = Column(Integer, primary_key=True)
    poem_id = Column(Integer, ForeignKey("poems.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)


class Favorite(Base):
    __tablename__ = "favorites"
    __table_args__ = (UniqueConstraint("user_id", "poem_id", name="uq_user_poem_favorite"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    poem_id = Column(Integer, ForeignKey("poems.id"), index=True, nullable=False)
    created_at = Column(DateTime, default=now, nullable=False)

    poem = relationship("Poem")


class BrowseHistory(Base):
    __tablename__ = "browse_history"
    __table_args__ = (UniqueConstraint("user_id", "poem_id", name="uq_user_poem_history"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    poem_id = Column(Integer, ForeignKey("poems.id"), index=True, nullable=False)
    viewed_at = Column(DateTime, default=now, nullable=False)

    poem = relationship("Poem")


class SquareTopic(Base, TimestampMixin):
    __tablename__ = "square_topics"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    title = Column(String(160), nullable=False)
    content = Column(Text, nullable=False)
    badge = Column(String(40), default="随笔", nullable=False)
    tags = Column(Text, default="[]", nullable=False)
    images = Column(Text, default="[]", nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    favorite_count = Column(Integer, default=0, nullable=False)
    share_count = Column(Integer, default=0, nullable=False)

    author = relationship("User")
    comments = relationship("SquareComment", cascade="all, delete-orphan")


class SquareComment(Base, TimestampMixin):
    __tablename__ = "square_comments"

    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(Integer, ForeignKey("square_topics.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    content = Column(Text, nullable=False)
    like_count = Column(Integer, default=0, nullable=False)
    favorite_count = Column(Integer, default=0, nullable=False)

    author = relationship("User")


class SquareReaction(Base):
    __tablename__ = "square_reactions"
    __table_args__ = (UniqueConstraint("user_id", "target_type", "target_id", "reaction_type", name="uq_square_reaction"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    target_type = Column(String(20), index=True, nullable=False)
    target_id = Column(Integer, index=True, nullable=False)
    reaction_type = Column(String(20), index=True, nullable=False)
    created_at = Column(DateTime, default=now, nullable=False)


class FeihualingRecord(Base):
    __tablename__ = "feihualing_records"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    keyword = Column(String(20), index=True, nullable=False)
    answer = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False, nullable=False)
    score = Column(Integer, default=0, nullable=False)
    source_title = Column(String(120), default="", nullable=False)
    source_author = Column(String(80), default="", nullable=False)
    source_dynasty = Column(String(40), default="", nullable=False)
    created_at = Column(DateTime, default=now, nullable=False)


class FeihualingRoom(Base, TimestampMixin):
    __tablename__ = "feihualing_rooms"

    id = Column(Integer, primary_key=True)
    creator_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    title = Column(String(120), nullable=False)
    keyword = Column(String(20), index=True, nullable=False)
    can_watch = Column(Boolean, default=True, nullable=False)
    player_count = Column(Integer, default=1, nullable=False)
    max_players = Column(Integer, default=4, nullable=False)
    round_text = Column(String(80), default="招募中", nullable=False)

    creator = relationship("User")
    messages = relationship("FeihualingRoomMessage", cascade="all, delete-orphan")


class FeihualingRoomMessage(Base, TimestampMixin):
    __tablename__ = "feihualing_room_messages"

    id = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("feihualing_rooms.id"), index=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    role = Column(String(20), default="opponent", nullable=False)
    content = Column(Text, nullable=False)
    source_title = Column(String(120), default="", nullable=False)
    source_author = Column(String(80), default="", nullable=False)
    source_dynasty = Column(String(40), default="", nullable=False)

    user = relationship("User")


class UserFollow(Base):
    __tablename__ = "user_follows"
    __table_args__ = (UniqueConstraint("user_id", "target_user_id", name="uq_user_follow"),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    target_user_id = Column(Integer, ForeignKey("users.id"), index=True, nullable=False)
    created_at = Column(DateTime, default=now, nullable=False)


class Feedback(Base):
    __tablename__ = "feedback"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    content = Column(Text, nullable=False)
    contact = Column(String(160), default="", nullable=False)
    status = Column(String(40), default="received", nullable=False)
    created_at = Column(DateTime, default=now, nullable=False)
