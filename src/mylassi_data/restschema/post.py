from __future__ import annotations

from pydantic import BaseModel


class PostRestType(BaseModel):
    id: int
    title: str
    author: str
