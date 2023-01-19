from __future__ import annotations

from pydantic import BaseModel


class ArticleRestType(BaseModel):
    id: int
    title: str
    author: str

    teaser: str | None = None


class ArticleOptionsRestType(BaseModel):
    title: str
    teaser: str | None = None
