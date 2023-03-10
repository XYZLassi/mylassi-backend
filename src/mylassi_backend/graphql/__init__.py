__all__ = ['graphql_app']

from typing import List, Optional

import strawberry
from sqlalchemy.orm import scoped_session, Session
from strawberry.fastapi import GraphQLRouter

from mylassi_data.db import SessionLocal
from mylassi_data.graphschema import *
from mylassi_data.models import *
from mylassi_tools.pagination import encode_cursor, decode_cursor


# noinspection PyTypeChecker
@strawberry.type
class Query:
    @strawberry.field
    def articles(self, cursor: Optional[str] = None, size: int = 5,
                 category: Optional[str] = None) -> PaginationResult[ArticleGraphType]:
        session: Session = scoped_session(SessionLocal)

        if size <= 0 or size > 50:
            size = 5

        query = ArticleModel.q(session)
        query = query.order_by(ArticleModel.id.desc())
        query = query.filter(ArticleModel.is_deleted_flag == None)

        if cursor and (cursor_id := decode_cursor(cursor)):
            query = query.filter(ArticleModel.id < cursor_id)

        if category:
            query = query.join(CategoryModel, ArticleModel.categories).filter(CategoryModel.unique_name == category)

        query_count = query.count()
        query = query.limit(size)
        items = query.all()

        return PaginationResult[ArticleGraphType](
            items=items,
            cursor=encode_cursor(items[-1].id) if len(items) > 0 and query_count > size else None,
            pageSize=size,
            length=len(items),
        )

    @strawberry.field
    def article_by_id(self, article: int) -> Optional[ArticleGraphType]:
        session: Session = scoped_session(SessionLocal)
        article = ArticleModel.get(session, article)
        assert not article.is_deleted
        return article

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
