from __future__ import annotations

from pydantic import BaseModel


class CategoryOptionRestType(BaseModel):
    category: str
    unique_name: str | None = None


class CategoryRestType(CategoryOptionRestType):
    id: int
