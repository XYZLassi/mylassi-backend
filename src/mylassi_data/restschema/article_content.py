from __future__ import annotations

from enum import Enum

from fastapi_camelcase import CamelModel


class ArticleContentType(str, Enum):
    header = 'header'
    text = 'text'


class ArticleContentOptionsRestType(CamelModel):
    content_type: ArticleContentType

    header: str | None = None
    text_content: str | None = None


class ArticleContentRestType(ArticleContentOptionsRestType):
    id: int
    position: int
