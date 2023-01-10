from __future__ import annotations

from pydantic import BaseModel


class UserRestType(BaseModel):
    id: int
    username: str
    email: str | None = None
    disabled: bool | None = None
