__all__ = ['graphql_app']

from typing import List, Union, Optional

import strawberry
from sqlalchemy.orm import scoped_session, Session
from strawberry.fastapi import GraphQLRouter

from mylassi_data.db import SessionLocal
from mylassi_data.models import *
from mylassi_data.graphschema import *


# noinspection PyTypeChecker
@strawberry.type
class Query:
    @strawberry.field
    def articles(self) -> List[ArticleGraphType]:
        session: Session = scoped_session(SessionLocal)
        return ArticleModel.q(session).all()

    @strawberry.field
    def article_by_id(self, article: int) -> Optional[ArticleGraphType]:
        session: Session = scoped_session(SessionLocal)
        return ArticleModel.get(session, article)

    @strawberry.field
    def authors(self) -> List[AuthorGraphType]:
        session: Session = scoped_session(SessionLocal)
        return UserModel.q(session).filter(UserModel.article_count > 0).all()

    @strawberry.field
    def categories(self) -> List[CategoryGraphType]:
        session: Session = scoped_session(SessionLocal)
        return CategoryModel.q(session).all()

    @strawberry.field
    def category_by_id(self, category: int) -> Optional[CategoryGraphType]:
        session: Session = scoped_session(SessionLocal)
        return CategoryModel.get(session, category)

    @strawberry.field
    def category_by_unique_name(self, category: str) -> Optional[CategoryGraphType]:
        session: Session = scoped_session(SessionLocal)
        return CategoryModel.get(session, category)


graphql_schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(graphql_schema)
