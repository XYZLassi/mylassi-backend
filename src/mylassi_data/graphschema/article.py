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
    id: strawberry.ID
    file_usage: Optional[str]
    filename: str
    url: str


@strawberry.type
class ArticleGraphType:
    id: strawberry.ID
    title: str

    teaser: Optional[str]

    author: Annotated["AuthorGraphType", strawberry.lazy(".author")]
    categories: List[Annotated["CategoryGraphType", strawberry.lazy(".category")]]

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
