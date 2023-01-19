from typing import Annotated, TYPE_CHECKING, List

import strawberry

if TYPE_CHECKING:
    from .article import ArticleGraphType


@strawberry.type
class AuthorGraphType:
    id: strawberry.ID
    username: str
    articles: List[Annotated["ArticleGraphType", strawberry.lazy(".article")]]
