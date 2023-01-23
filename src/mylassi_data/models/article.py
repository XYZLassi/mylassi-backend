__all__ = ['ArticleModel', 'ArticleFileModel']

import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base
from mylassi_data.models.mixins import CategoryMixin
from mylassi_data.restschema import *

if TYPE_CHECKING:
    from .file import FileModel
    from .user import UserModel


class ArticleFileModel(Base, ModelMixin):
    __tablename__ = "articles_files_associations"
    id: int = Column(Integer, primary_key=True, index=True)
    article_id: int = Column(ForeignKey("articles.id"), nullable=False)

    file_usage: Optional[str] = Column(String, nullable=True)

    file_id: str = Column(ForeignKey("files.id"), nullable=False)
    file: 'FileModel' = relationship("FileModel")

    def set_from_rest_type(self, options: ArticleFileOptionsRestType):
        self.file_usage = options.file_usage

    def rest_type(self) -> ArticleFileRestType:
        return ArticleFileRestType(
            id=self.id,
            file_usage=self.file_usage,
            file=self.file_id
        )


class ArticleModel(Base, ModelMixin, CategoryMixin):
    __tablename__ = "articles"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, nullable=False)

    time_created: datetime.datetime = Column(DateTime(timezone=True), server_default=func.now())

    teaser: Optional[str] = Column(Text, nullable=True)

    author_id: int = Column(Integer, ForeignKey("users.id"))
    author: 'UserModel' = relationship("UserModel", back_populates="articles")

    file_associations: List['ArticleFileModel'] = relationship('ArticleFileModel')
    files: List['FileModel'] = relationship("FileModel", lazy='dynamic',
                                            viewonly=True, secondary=ArticleFileModel.__table__)

    def set_from_rest_type(self, options: ArticleOptionsRestType):
        self.title = options.title
        self.teaser = options.teaser

    def rest_type(self) -> ArticleRestType:
        return ArticleRestType(
            id=self.id,
            title=self.title,
            author=self.author_id,
            categories=[c.id for c in self.categories],
            teaser=self.teaser,
        )
