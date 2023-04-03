__all__ = ['create_app']

from dotenv import load_dotenv
from fastapi import FastAPI


def create_app() -> FastAPI:
    load_dotenv('.env')
    app = FastAPI(title="MyLassi.xyz - API")

    from .api import api_v1
    app.mount('/api', api_v1)

    return app
