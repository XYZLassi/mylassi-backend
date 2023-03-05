from typing import List

from fastapi_camelcase import CamelModel


class AuthorRestType(CamelModel):
    id: int
    username: str
    articles: List[int]
