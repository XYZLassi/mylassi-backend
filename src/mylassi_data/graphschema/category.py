from typing import TYPE_CHECKING, Annotated, List

import strawberry
from mylassi_data.models import *

if TYPE_CHECKING:
    from .article import ArticleGraphType


@strawberry.type
class CategoryGraphType:
    id: strawberry.ID
    category: str

    @strawberry.field
    def articles(self) -> List[Annotated["ArticleGraphType", strawberry.lazy(".article")]]:
        query = ArticleModel.q().filter(ArticleModel.categories.any(CategoryModel.id == self.id))
        return query.all()
