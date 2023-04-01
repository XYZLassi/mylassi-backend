import datetime
import os
from typing import Optional

from sqlalchemy import Column, Integer, Boolean, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from werkzeug.utils import secure_filename

from mylassi_backend.tools import ModelMixin
from mylassi_data.db import Base
from mylassi_data.restschema import FileRestType

SERVER_PREFIX = os.environ.get('SERVER_PREFIX', '/')


class FSFileModel(Base, ModelMixin):
    __tablename__ = "fs_files"
    id: int = Column(Integer, primary_key=True, index=True)
    ready: bool = Column(Boolean, nullable=False, default=False, server_default='0')
    hash_value: str = Column(String, nullable=True, unique=True)

    mimetype: str = Column(String, nullable=False)

    image_width: Optional[int] = Column(Integer, nullable=True)
    image_height: Optional[int] = Column(Integer, nullable=True)

    on_created: datetime.datetime = Column(DateTime, nullable=False, server_default=func.now())
    on_updated: datetime.datetime = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())

    @property
    def save_origin_filename(self) -> str:
        return secure_filename(self.origin_filename)

    @property
    def path(self) -> str:
        return os.path.join(str(self.id), f'{self.id}.dat')

    @property
    def is_image(self) -> bool:
        return self.mimetype.startswith('image/')


class FileModel(Base, ModelMixin):
    __tablename__ = "files"

    id: str = Column(String, primary_key=True, index=True, default=ModelMixin.generate_uuid)
    origin_filename: str = Column(String, nullable=False)
    filename: str = Column(String, nullable=False)

    fs_model_id: int = Column(Integer, ForeignKey("fs_files.id"), nullable=False)
    fs_model: FSFileModel = relationship("FSFileModel")

    owner_id: int = Column(Integer, ForeignKey("users.id"))
    owner = relationship("UserModel")

    @property
    def save_filename(self) -> str:
        return secure_filename(self.filename)

    @property
    def path(self):
        return self.fs_model.path

    @property
    def is_image(self) -> bool:
        return self.fs_model.is_image

    @property
    def url(self) -> str:
        if self.is_image:
            return os.path.join(SERVER_PREFIX, 'images', self.id)

        return os.path.join(SERVER_PREFIX, 'files', self.id)  # Todo: dynamic

    def rest_type(self) -> FileRestType:
        return FileRestType(
            id=self.id,
            filename=self.filename,
            url=self.url,
            mimetype=self.fs_model.mimetype,
            image_height=self.fs_model.image_height,
            image_width=self.fs_model.image_width
        )
