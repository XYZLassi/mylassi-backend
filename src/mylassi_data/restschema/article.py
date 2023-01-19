from __future__ import annotations

from pydantic import BaseModel


class ArticleOptionsRestType(BaseModel):
    title: str
    teaser: str | None = None


class ArticleRestType(ArticleOptionsRestType):
    id: int
    title: str
    teaser: str | None = None

    author: int
    categories: list[int] = []
