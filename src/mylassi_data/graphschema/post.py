import datetime
from typing import Annotated, TYPE_CHECKING, Optional

import strawberry

if TYPE_CHECKING:
    from .author import AuthorGraphType


@strawberry.type
class PostGraphType:
    id: strawberry.ID
    title: str

    teaser: Optional[str]

    author: Annotated["AuthorGraphType", strawberry.lazy(".author")]
    time_created: datetime.datetime
