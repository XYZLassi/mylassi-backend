from typing import List

from pydantic import BaseModel


class AuthorRestType(BaseModel):
    id: int
    username: str
    posts: List[str]
