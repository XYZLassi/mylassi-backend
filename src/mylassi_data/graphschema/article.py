import datetime
from typing import Annotated, TYPE_CHECKING, Optional, List

import strawberry

from .dataclasses import *
from ..models import ArticleModel

if TYPE_CHECKING:
    from .author import AuthorGraphType
    from .category import CategoryGraphType


@strawberry.type
class ArticleFileGraphType:
    file_id: str
    article_file_id: int
    file_usage: Optional[str]
    filename: str
    url: str
    href: str

    mimetype: str
    image_width: Optional[int]
    image_height: Optional[int]


@strawberry.type
class ArticleContentGraphType:
    id: int
    position: int
    content_type: str

    header: str


@strawberry.type
class ArticleGraphType:
    id: int
    title: str

    teaser: Optional[str]

    author: Annotated["AuthorGraphType", strawberry.lazy(".author")]
    categories: List[Annotated["CategoryGraphType", strawberry.lazy(".category")]]

    contents: List[ArticleContentGraphType]

    time_created: datetime.datetime

    @strawberry.field
    def files_by_usage(self: ArticleModel, usage: str) -> List[ArticleFileGraphType]:
        for association in self.file_associations:
            if association.file_usage != usage:
                continue
            yield ArticleFileGraphReturnType.from_model(association)

    @strawberry.field
    def files(self: ArticleModel) -> List[ArticleFileGraphType]:
        for association in self.file_associations:
            yield ArticleFileGraphReturnType.from_model(association)
