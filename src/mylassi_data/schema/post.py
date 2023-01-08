import datetime
from typing import Annotated, TYPE_CHECKING

import strawberry

if TYPE_CHECKING:
    from .author import Author


@strawberry.type
class Post:
    id: strawberry.ID
    title: str
    author: Annotated["Author", strawberry.lazy(".author")]
    content: str
    time_created: datetime.datetime
