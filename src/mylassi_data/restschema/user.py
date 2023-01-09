from __future__ import annotations

from pydantic import BaseModel


class UserRestType(BaseModel):
    username: str
    email: str | None = None
