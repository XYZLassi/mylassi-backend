__all__ = ['api_v1']

from fastapi import FastAPI

version = '0.11.0'
title = "MyLassi.xyz - API V1"
api_v1 = FastAPI(title=title, version=version)

from .graphql import graphql_app

api_v1.include_router(graphql_app, prefix="/graphql", include_in_schema=False)

from .security import router as security_router

api_v1.include_router(security_router)

from .article import router as article_router

api_v1.include_router(article_router)

from .author import router as author_router

api_v1.include_router(author_router)

from .file import router as file_router

api_v1.include_router(file_router)

from .category import router as category_router

api_v1.include_router(category_router)
