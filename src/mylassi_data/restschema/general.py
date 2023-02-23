from pydantic import BaseModel


class OkayResultRestType(BaseModel):
    okay: bool
