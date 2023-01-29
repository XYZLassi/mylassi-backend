from sqlalchemy import Column, Integer, String

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base
from mylassi_data.restschema import CategoryRestType, CategoryOptionRestType


class CategoryModel(Base, ModelMixin):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    category = Column(String, nullable=False)

    def set_from_rest_type(self, options: CategoryOptionRestType):
        self.category = options.category

    def rest_type(self) -> CategoryRestType:
        return CategoryRestType(
            id=self.id,
            category=self.category,
        )
