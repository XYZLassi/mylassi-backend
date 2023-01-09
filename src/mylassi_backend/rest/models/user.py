from __future__ import annotations

from pydantic import BaseModel


class User(BaseModel):
    username: str
    email: str | None = None
