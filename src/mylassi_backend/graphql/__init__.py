__all__ = ['graphql_app']

from typing import List

import strawberry
from sqlalchemy.orm import scoped_session, Session
from strawberry.fastapi import GraphQLRouter

from mylassi_data.db import SessionLocal
from mylassi_data.models import *
from mylassi_data.graphschema import *

# noinspection PyTypeChecker
db_session: Session = scoped_session(SessionLocal)


@strawberry.type
class Query:
    @strawberry.field
    def articles(self) -> List[ArticleGraphType]:
        return ArticleModel.q(db_session).all()

    @strawberry.field
    def authors(self) -> List[AuthorGraphType]:
        return UserModel.q(db_session).filter(UserModel.article_count > 0).all()

    @strawberry.field()
    def categories(self) -> List[CategoryGraphType]:
        return CategoryModel.q(db_session).all()


graphql_schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(graphql_schema)
