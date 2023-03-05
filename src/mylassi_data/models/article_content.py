__all__ = ['ArticleContentModel']

from typing import Optional

from sqlalchemy import Column, Integer, ForeignKey, String

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base
from mylassi_data.restschema import ArticleContentRestType, ArticleContentType, ArticleContentOptionsRestType


class ArticleContentModel(Base, ModelMixin):
    __tablename__ = "article_contents"

    id: int = Column(Integer, primary_key=True, index=True)
    position: int = Column(Integer, nullable=False)

    article_id: int = Column(ForeignKey("articles.id"), nullable=False)

    content_type: str = Column(String, nullable=False)

    header: Optional[str] = Column(String, nullable=True)

    def set_from_rest_type(self, options: ArticleContentOptionsRestType):
        self.content_type = options.content_type
        self.header = options.header

    def rest_type(self) -> ArticleContentRestType:
        return ArticleContentRestType(
            id=self.id,
            position=self.position,
            content_type=ArticleContentType(self.content_type),
            header=self.header
        )
