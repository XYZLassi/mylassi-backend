__all__ = ['create_app']

from dotenv import load_dotenv
from fastapi import FastAPI

version = '0.3.0'


def create_app() -> FastAPI:
    load_dotenv('.env')
    app = FastAPI(version=version, title="MyLassi.xyz - API")

    from .graphql import graphql_app
    app.include_router(graphql_app, prefix="/graphql", include_in_schema=False)

    from .rest.security import router as security_router
    app.include_router(security_router)

    from .rest.article import router as article_router
    app.include_router(article_router)

    from .rest.author import router as author_router
    app.include_router(author_router)

    from .rest.file import router as file_router
    app.include_router(file_router)

    from .rest.category import router as category_router
    app.include_router(category_router)

    return app
