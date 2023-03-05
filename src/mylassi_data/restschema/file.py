from enum import Enum
from typing import Optional

from fastapi_camelcase import CamelModel


class ImageFormatType(str, Enum):
    jpeg = 'jpeg'
    png = 'png'
    webp = 'webp'


class FileRestType(CamelModel):
    id: str
    filename: str
    url: str

    mimetype: str
    image_width: Optional[int]
    image_height: Optional[int]
