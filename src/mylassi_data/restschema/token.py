from fastapi_camelcase import CamelModel


class TokenRestType(CamelModel):
    access_token: str
    token_type: str
