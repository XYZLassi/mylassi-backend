from typing import TYPE_CHECKING

import strawberry

if TYPE_CHECKING:
    pass


@strawberry.type
class FileGraphType:
    id: strawberry.ID
