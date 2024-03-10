__all__ = ['create_app']

import os

from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse

from mylassi_data.db import Base, engine

general_router = APIRouter()


@general_router.get('/', include_in_schema=False)
def index_redirect():
    return RedirectResponse('/api/docs')


def create_app() -> FastAPI:
    app = FastAPI(title="MyLassi.xyz - API")

    bind(app)

    # General
    app.include_router(general_router)

    from .api import api_v1
    app.mount('/api', api_v1)

    return app


def bind(app: FastAPI):
    @app.on_event("startup")
    def on_startup() -> None:
        if os.environ.get('CREATE_DB', 'True') == 'True':
            Base.metadata.create_all(bind=engine)
