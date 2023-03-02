from enum import Enum

from pydantic import BaseModel


class ArticleContentType(str, Enum):
    header = 'header'


class ArticleContentOptionsRestType(BaseModel):
    content_type: ArticleContentType


class ArticleContentRestType(ArticleContentOptionsRestType):
    id: int
    position: int
