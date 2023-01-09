from __future__ import annotations

from pydantic import BaseModel


class Post(BaseModel):
    id: int
    title: str
    author: str
