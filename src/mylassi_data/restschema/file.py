from pydantic import BaseModel


class FileRestType(BaseModel):
    id: str
    filename: str
    url: str
