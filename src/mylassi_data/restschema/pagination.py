from typing import Generic, TypeVar, List, Optional

from pydantic.generics import GenericModel

T = TypeVar('T')


class PaginationResultRestType(GenericModel, Generic[T]):
    items: List[T]
    pageSize: int
    length: int
    cursor: Optional[str]
