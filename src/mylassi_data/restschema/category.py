from pydantic import BaseModel


class CategoryOptionRestType(BaseModel):
    category: str


class CategoryRestType(CategoryOptionRestType):
    id: int
