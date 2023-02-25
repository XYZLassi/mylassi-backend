from dataclasses import dataclass
from typing import Generic, TypeVar, List, Optional

import strawberry

T = TypeVar('T')


@strawberry.type
@dataclass
class PaginationResult(Generic[T]):
    items: List[T]
    size: int
    cursor: Optional[str]
