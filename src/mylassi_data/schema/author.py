from typing import Annotated, TYPE_CHECKING, List

import strawberry

if TYPE_CHECKING:
    from .post import Post


@strawberry.type
class Author:
    username: str
    posts: List[Annotated["Post", strawberry.lazy(".post")]]
