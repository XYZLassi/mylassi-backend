from pydantic import BaseModel


class TokenRestType(BaseModel):
    access_token: str
    token_type: str
