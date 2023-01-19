import os

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base


class FileModel(Base, ModelMixin):
    __tablename__ = "files"

    id: int = Column(Integer, primary_key=True, index=True)
    ready: bool = Column(Boolean, nullable=False, default=False, server_default='0')
    filename: str = Column(String, nullable=False)

    owner_id: int = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel")

    @property
    def save_filename(self) -> str:
        return secure_filename(self.filename)

    @property
    def path(self) -> str:
        return os.path.join(str(self.id), self.save_filename)
