from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import declared_attr, relationship

from mylassi_data.db import Base


class CategoryMixin:
    @declared_attr
    def categories(self):
        table_name = self.__tablename__
        association_table = Table(
            f'{table_name}_categories_associations',
            Base.metadata,
            Column('item_id', ForeignKey(f"{table_name}.id", ondelete="CASCADE"), nullable=False),
            Column('category_id', ForeignKey("categories.id"), nullable=False),
        )

        return relationship("CategoryModel", lazy='dynamic', secondary=association_table)
