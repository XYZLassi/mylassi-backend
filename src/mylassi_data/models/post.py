__all__ = ['PostModel']

import datetime
from typing import Optional

from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship

from mylassi_data.db import Base

from mylassi_backend.tools import ModelMixin

from mylassi_data.restschema import PostRestType, PostOptionsRestType


class PostModel(Base, ModelMixin):
    __tablename__ = "posts"

    id: int = Column(Integer, primary_key=True, index=True)
    title: str = Column(String, nullable=False)

    time_created: datetime.datetime = Column(DateTime(timezone=True), server_default=func.now())

    teaser: Optional[str] = Column(Text, nullable=True)

    author_id: int = Column(Integer, ForeignKey("users.id"))
    author = relationship("UserModel", back_populates="posts")

    def set_from_rest_type(self, options: PostOptionsRestType):
        self.title = options.title
        self.teaser = options.teaser

    def rest_type(self) -> PostRestType:
        return PostRestType(
            id=self.id,
            title=self.title,
            author=f'/author/{self.author_id}',
            teaser=self.teaser,
        )
