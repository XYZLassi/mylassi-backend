from __future__ import annotations

from sqlalchemy import Column, Integer, String, Boolean, select, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship, object_session

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base

from werkzeug.security import generate_password_hash, check_password_hash


class User(Base, ModelMixin):
    __tablename__ = 'users'

    id: int = Column(Integer, primary_key=True)
    username: str = Column(String, index=True, unique=True)
    email: str = Column(String, index=True, unique=True)
    password_hash: str = Column(String)
    is_admin: bool = Column(Boolean, server_default="0", default=False, nullable=False)

    posts = relationship("Post", back_populates="author", lazy="dynamic")

    @hybrid_property
    def post_count(self):
        from .post import Post
        return object_session(self).query(Post).filter(Post.author == self).count()

    @post_count.expression
    def post_count(cls):
        from .post import Post
        return select([func.count(Post.id)]).where(Post.author_id == cls.id).label('post_count')

    @classmethod
    def get_by_username(cls, username) -> User:
        return cls.first(username=username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
