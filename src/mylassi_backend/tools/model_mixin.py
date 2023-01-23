import uuid
from typing import Type, TypeVar, Iterator, Optional

from fastapi import HTTPException
from sqlalchemy.orm import Query, Session

T = TypeVar('T')


class ModelMixin:
    @staticmethod
    def generate_uuid():
        return str(uuid.uuid4())

    @classmethod
    def q(cls: Type[T], session: Session, **kwargs) -> Query:
        q: Query = session.query(cls)
        return q

    @classmethod
    def all(cls: Type[T], session: Session, **kwargs) -> Iterator[T]:
        q: Query = cls.q(session)
        for item in q.filter_by(**kwargs):
            yield item

    @classmethod
    def get(cls: Type[T], session: Session, doc_id) -> Optional[T]:
        q: Query = cls.q(session)
        item: Optional[T] = q.get(doc_id)
        return item

    @classmethod
    def get_or_404(cls: Type[T], session: Session, doc_id) -> T:
        q: Query = cls.q(session)
        item = q.get(doc_id)

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        return item

    @classmethod
    def first(cls: Type[T], session: Session, **kwargs) -> Optional[T]:
        q: Query = cls.q(session)
        item: Optional[T] = q.filter_by(**kwargs).first()
        return item
