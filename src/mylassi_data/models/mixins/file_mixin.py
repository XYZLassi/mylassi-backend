from sqlalchemy import Column, Table, ForeignKey
from sqlalchemy.orm import declared_attr, relationship

from mylassi_data.db import Base


class FileMixin:
    @declared_attr
    def files(self):
        table_name = self.__tablename__
        association_table = Table(
            f'{table_name}_files_associations',
            Base.metadata,
            Column('item_id', ForeignKey(f"{table_name}.id", ondelete="CASCADE"), nullable=False),
            Column('file_id', ForeignKey("files.id"), nullable=False),
        )

        return relationship("FileModel", lazy='dynamic', secondary=association_table)
