__all__ = ['PostModel']

import datetime

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey
from sqlalchemy.orm import relationship

from mylassi_data.db import Base

from mylassi_backend.tools import ModelMixin

from mylassi_data.restschema import PostRestType


class PostModel(Base, ModelMixin):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String)

    time_created: datetime.datetime = Column(DateTime(timezone=True), server_default=func.now())

    author_id: int = Column(Integer, ForeignKey("users.id"))
    author = relationship("UserModel", back_populates="posts")

    def rest_type(self) -> PostRestType:
        return PostRestType(
            id=self.id,
            title=self.title,
            author=f'/author/{self.author_id}'
        )
