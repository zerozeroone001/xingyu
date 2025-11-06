"""Pydantic Schema"""

from app.schemas.user import (
    UserCreate,
    UserUpdate,
    UserResponse,
    UserLogin,
    UserRegister,
)
from app.schemas.author import (
    AuthorCreate,
    AuthorUpdate,
    AuthorResponse,
    AuthorSimple,
)
from app.schemas.poetry import (
    PoetryCreate,
    PoetryUpdate,
    PoetryResponse,
    PoetryDetail,
    PoetryListItem,
    PoetryQuery,
)
from app.schemas.response import ResponseModel, PaginatedResponse

__all__ = [
    "UserCreate",
    "UserUpdate",
    "UserResponse",
    "UserLogin",
    "UserRegister",
    "AuthorCreate",
    "AuthorUpdate",
    "AuthorResponse",
    "AuthorSimple",
    "PoetryCreate",
    "PoetryUpdate",
    "PoetryResponse",
    "PoetryDetail",
    "PoetryListItem",
    "PoetryQuery",
    "ResponseModel",
    "PaginatedResponse",
]
