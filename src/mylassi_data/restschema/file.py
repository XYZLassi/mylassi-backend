from typing import Optional

from pydantic import BaseModel


class FileRestType(BaseModel):
    id: str
    filename: str
    url: str

    mimetype: str
    image_width: Optional[int]
    image_height: Optional[int]
