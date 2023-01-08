__all__ = ['graphql_app']

from typing import List

import strawberry
from strawberry.fastapi import GraphQLRouter

import mylassi_data.models as model
import mylassi_data.schema as schema


@strawberry.type
class Query:
    @strawberry.field
    def posts(self) -> List[schema.Post]:
        return model.Post.query.all()

    @strawberry.field
    def authors(self) -> List[schema.Author]:
        return model.User.query.filter(model.User.post_count > 0).all()


graphql_schema = strawberry.Schema(Query)

graphql_app = GraphQLRouter(graphql_schema)
