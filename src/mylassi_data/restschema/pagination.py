from typing import Generic, TypeVar, List, Optional

from fastapi_camelcase import CamelModel
from pydantic.generics import GenericModel

T = TypeVar('T')


class PaginationResultRestType(GenericModel, CamelModel, Generic[T]):
    items: List[T]
    pageSize: int
    length: int
    cursor: Optional[str]
