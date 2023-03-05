from fastapi_camelcase import CamelModel


class OkayResultRestType(CamelModel):
    okay: bool
