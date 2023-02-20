import datetime

from sqlalchemy import Column, DateTime
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import declared_attr


class CanDeleteMixin:
    @declared_attr
    def is_deleted_flag(self):
        return Column(DateTime, nullable=True)

    @hybrid_property
    def is_deleted(self) -> bool:
        return self.is_deleted_flag != None

    @is_deleted.setter
    def is_deleted(self, value: bool):
        assert isinstance(value, bool)
        if value:
            # noinspection PyAttributeOutsideInit
            self.is_deleted_flag = datetime.datetime.utcnow()
        else:
            # noinspection PyAttributeOutsideInit
            self.is_deleted_flag = None

    @is_deleted.expression
    def is_deleted(self):
        return self.is_deleted_flag != None
