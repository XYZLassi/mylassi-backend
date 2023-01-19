__all__ = ['create_app']

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

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

    return app
