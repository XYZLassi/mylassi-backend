__all__ = ['ArticleContentModel']

from sqlalchemy import Column, Integer, ForeignKey, String

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base


class ArticleContentModel(Base, ModelMixin):
    __tablename__ = "article_contents"

    id: int = Column(Integer, primary_key=True, index=True)
    position: int = Column(Integer, nullable=False)

    article_id: int = Column(ForeignKey("articles.id"), nullable=False)

    content_type: str = Column(String, nullable=False)
