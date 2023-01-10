from __future__ import annotations

from pydantic import BaseModel


class PostRestType(BaseModel):
    id: int
    title: str
    author: str

    teaser: str | None = None


class PostOptionsRestType(BaseModel):
    title: str
    teaser: str | None = None
