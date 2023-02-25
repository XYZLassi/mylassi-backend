from typing import TYPE_CHECKING, Annotated, List, Optional

import strawberry
from sqlalchemy.orm import Session, scoped_session

from mylassi_data.models import *
from ..db import SessionLocal

if TYPE_CHECKING:
    from .article import ArticleGraphType


@strawberry.type
class CategoryGraphType:
    id: strawberry.ID
    category: str
    unique_name: Optional[str]

    @strawberry.field(deprecation_reason='It will be remove or changed in future update')
    def articles(self) -> List[Annotated["ArticleGraphType", strawberry.lazy(".article")]]:
        # noinspection PyTypeChecker
        session: Session = scoped_session(SessionLocal)
        query = ArticleModel.q(session).filter(ArticleModel.categories.any(CategoryModel.id == self.id))
        return query.all()
