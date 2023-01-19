__all__ = ['graphql_app']

from typing import List

import strawberry
from strawberry.fastapi import GraphQLRouter

from mylassi_data.models import *
from mylassi_data.graphschema import *


@strawberry.type
class Query:
    @strawberry.field
    def articles(self) -> List[ArticleGraphType]:
        return ArticleModel.query.all()

    @strawberry.field
    def authors(self) -> List[AuthorGraphType]:
        return UserModel.query.filter(UserModel.article_count > 0).all()


graphql_schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(graphql_schema)
