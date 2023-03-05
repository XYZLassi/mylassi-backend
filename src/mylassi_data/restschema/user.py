from __future__ import annotations

from fastapi_camelcase import CamelModel


class UserRestType(CamelModel):
    id: int
    username: str
    email: str | None = None
    disabled: bool | None = None
