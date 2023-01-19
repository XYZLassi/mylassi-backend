from __future__ import annotations

from sqlalchemy import Column, Integer, String, Boolean, select, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, object_session

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base

from werkzeug.security import generate_password_hash, check_password_hash

from mylassi_data.restschema import UserRestType, AuthorRestType


class UserModel(Base, ModelMixin):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String, index=True, unique=True)
    email: str = Column(String, index=True, unique=True)
    password_hash: str = Column(String)
    disabled: bool = Column(Boolean, server_default="0", default=False, nullable=False)
    is_admin: bool = Column(Boolean, server_default="0", default=False, nullable=False)

    articles = relationship("ArticleModel", back_populates="author", lazy="dynamic")

    @hybrid_property
    def article_count(self):
        from .article import ArticleModel
        return object_session(self).query(ArticleModel).filter(ArticleModel.author == self).count()

    @article_count.expression
    def article_count(cls):
        from .article import ArticleModel
        return select([func.count(ArticleModel.id)]).where(ArticleModel.author_id == cls.id).label('article_count')

    @classmethod
    def get_by_username(cls, username) -> UserModel:
        return cls.first(username=username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def rest_type(self, all_data: bool = False) -> UserRestType:
        return UserRestType(
            id=self.id,
            username=self.username,
            email=self.email if all_data else None,
            disabled=self.disabled if all_data else None
        )

    def rest_type_author(self) -> AuthorRestType:
        return AuthorRestType(
            id=self.id,
            username=self.username,
            articles=[p.id for p in self.articles]
        )
