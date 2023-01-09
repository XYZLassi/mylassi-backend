__all__ = ['create_app']

from fastapi import FastAPI


def create_app() -> FastAPI:
    app = FastAPI()

    from .graphql import graphql_app
    app.include_router(graphql_app, prefix="/graphql")

    from .rest.security import router as security_router
    app.include_router(security_router)

    return app
