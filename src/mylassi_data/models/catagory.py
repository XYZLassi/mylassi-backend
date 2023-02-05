from __future__ import annotations

from typing import Union, Optional

from fastapi import HTTPException
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Session, Query

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base
from mylassi_data.restschema import CategoryRestType, CategoryOptionRestType


class CategoryModel(Base, ModelMixin):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)
    unique_name = Column(String, nullable=True, unique=True)

    def set_from_rest_type(self, options: CategoryOptionRestType):
        self.category = options.category
        self.unique_name = options.unique_name.lower()

    def rest_type(self) -> CategoryRestType:
        return CategoryRestType(
            id=self.id,
            category=self.category,
            unique_name=self.unique_name,
        )

    @classmethod
    def get_or_404(cls, session: Session, doc_id: Union[int, str]) -> CategoryModel:
        q: Query = cls.q(session)
        item: Optional[CategoryModel] = None

        if isinstance(doc_id, int):
            item = q.get(doc_id)
        elif isinstance(doc_id, str):
            item = q.filter_by(unique_name=doc_id.lower()).first()

        if not item:
            raise HTTPException(status_code=404, detail="Item not found")

        return item
