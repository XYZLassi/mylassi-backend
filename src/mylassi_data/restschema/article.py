from __future__ import annotations

import datetime
from enum import Enum
from typing import List

from fastapi_camelcase import CamelModel


class ArticleFileUsage(str, Enum):
    thumbnail = 'thumbnail'


class ArticleFileOptionsRestType(CamelModel):
    file_usage: ArticleFileUsage | None = None


class AppendArticleFileOptionsRestType(ArticleFileOptionsRestType):
    file_id: str
    file_usage: ArticleFileUsage | None = None


class ArticleFileRestType(AppendArticleFileOptionsRestType):
    article_file_id: int
    url: str


class ArticleOptionsRestType(CamelModel):
    title: str
    teaser: str | None = None


class ArticleRestType(ArticleOptionsRestType):
    id: int
    title: str
    teaser: str | None = None

    author: int
    categories: List[int] = []

    contents: List[int] = []


class FullArticleRestType(ArticleRestType):
    is_deleted: datetime.datetime | None = None
    article_files: List[ArticleFileRestType] = []
