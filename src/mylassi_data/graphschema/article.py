import datetime
from typing import Annotated, TYPE_CHECKING, Optional, List

import strawberry

if TYPE_CHECKING:
    from .author import AuthorGraphType
    from .category import CategoryGraphType


@strawberry.type
class ArticleGraphType:
    id: strawberry.ID
    title: str

    teaser: Optional[str]

    author: Annotated["AuthorGraphType", strawberry.lazy(".author")]
    categories: List[Annotated["CategoryGraphType", strawberry.lazy(".category")]]

    time_created: datetime.datetime
