from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class ArticleFileUsage(str, Enum):
    thumbnail = 'thumbnail'


class ArticleFileOptionsRestType(BaseModel):
    file_usage: ArticleFileUsage | None = None


class ArticleFileRestType(ArticleFileOptionsRestType):
    id: int
    file: int


class ArticleOptionsRestType(BaseModel):
    title: str
    teaser: str | None = None


class ArticleRestType(ArticleOptionsRestType):
    id: int
    title: str
    teaser: str | None = None

    author: int
    categories: list[int] = []
