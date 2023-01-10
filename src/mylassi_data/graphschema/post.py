import datetime
from typing import Annotated, TYPE_CHECKING

import strawberry

if TYPE_CHECKING:
    from .author import AuthorGraphType


@strawberry.type
class PostGraphType:
    id: strawberry.ID
    title: str
    author: Annotated["AuthorGraphType", strawberry.lazy(".author")]
    time_created: datetime.datetime
