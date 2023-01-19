__all__ = ['ArticleModel']

import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text, Table
from sqlalchemy.orm import relationship

from mylassi_data.db import Base

from mylassi_backend.tools import ModelMixin

from mylassi_data.restschema import ArticleRestType, ArticleOptionsRestType


class ArticleModel(Base, ModelMixin):
    __tablename__ = "articles"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, nullable=False)

    time_created: datetime.datetime = Column(DateTime(timezone=True), server_default=func.now())

    teaser: Optional[str] = Column(Text, nullable=True)

    author_id: int = Column(Integer, ForeignKey("users.id"))
    author = relationship("UserModel", back_populates="posts")

    def set_from_rest_type(self, options: ArticleOptionsRestType):
        self.title = options.title
        self.teaser = options.teaser

    def rest_type(self) -> ArticleRestType:
        return ArticleRestType(
            id=self.id,
            title=self.title,
            author=f'/author/{self.author_id}',
            teaser=self.teaser,
        )
