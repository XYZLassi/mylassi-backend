from __future__ import annotations

from fastapi_camelcase import CamelModel


class CategoryOptionRestType(CamelModel):
    category: str
    unique_name: str | None = None


class CategoryRestType(CategoryOptionRestType):
    id: int
