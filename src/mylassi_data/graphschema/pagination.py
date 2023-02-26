from dataclasses import dataclass
from typing import Generic, TypeVar, List, Optional

import strawberry

T = TypeVar('T')


@strawberry.type
@dataclass
class PaginationResult(Generic[T]):
    items: List[T]
    pageSize: int
    length: int
    cursor: Optional[str]
