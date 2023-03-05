from __future__ import annotations

from enum import Enum

from pydantic import BaseModel


class ArticleContentType(str, Enum):
    header = 'header'


class ArticleContentOptionsRestType(BaseModel):
    content_type: ArticleContentType

    header: str | None = None


class ArticleContentRestType(ArticleContentOptionsRestType):
    id: int
    position: int
