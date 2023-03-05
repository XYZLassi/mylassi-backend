from enum import Enum
from typing import Optional

from pydantic import BaseModel


class ImageFormatType(str, Enum):
    jpeg = 'jpeg'
    png = 'png'
    webp = 'webp'


class FileRestType(BaseModel):
    id: str
    filename: str
    url: str

    mimetype: str
    image_width: Optional[int]
    image_height: Optional[int]
