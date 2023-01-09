from typing import Type, TypeVar, Iterator, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Query

T = TypeVar('T')


class ModelMixin:
    @classmethod
    def q(cls: Type[T], **kwargs) -> Query:
        q: Query = cls.query
        return q

    @classmethod
    def all(cls: Type[T], **kwargs) -> Iterator[T]:
        q: Query = cls.query
        for item in q.filter_by(**kwargs):
            yield item

    @classmethod
    def get(cls: Type[T], doc_id) -> Optional[T]:
        q: Query = cls.query
        item: Optional[T] = q.get(doc_id)
        return item

    @classmethod
    def get_or_404(cls: Type[T], doc_id) -> T:
        item = cls.get(doc_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        return item

    @classmethod
    def first(cls: Type[T], **kwargs) -> Optional[T]:
        q: Query = cls.query
        item: Optional[T] = q.filter_by(**kwargs).first()
        return item
