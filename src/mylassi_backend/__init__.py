__all__ = ['create_app']

from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter
from fastapi.responses import RedirectResponse

general_router = APIRouter()


@general_router.get('/', include_in_schema=False)
def index_redirect():
    return RedirectResponse('/api/docs')


def create_app() -> FastAPI:
    load_dotenv('.env')
    app = FastAPI(title="MyLassi.xyz - API")

    # General
    app.include_router(general_router)

    from .api import api_v1
    app.mount('/api', api_v1)

    return app
