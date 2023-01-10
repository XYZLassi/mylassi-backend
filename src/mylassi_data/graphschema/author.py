from typing import Annotated, TYPE_CHECKING, List

import strawberry

if TYPE_CHECKING:
    from .post import PostGraphType


@strawberry.type
class AuthorGraphType:
    id: strawberry.ID
    username: str
    posts: List[Annotated["PostGraphType", strawberry.lazy(".post")]]
