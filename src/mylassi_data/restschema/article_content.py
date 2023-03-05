from __future__ import annotations

from enum import Enum

from fastapi_camelcase import CamelModel


class ArticleContentType(str, Enum):
    header = 'header'


class ArticleContentOptionsRestType(CamelModel):
    content_type: ArticleContentType

    header: str | None = None


class ArticleContentRestType(ArticleContentOptionsRestType):
    id: int
    position: int
