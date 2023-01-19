__all__ = ['router']

from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException

from mylassi_data.restschema import *
from mylassi_data.models import *

from mylassi_data import db

from .security import get_current_active_user

router = APIRouter(tags=['Articles'], prefix='/articles')


@router.get("/", response_model=List[ArticleRestType])
async def get_articles():
    return [p.rest_type() for p in ArticleModel.all()]


@router.post("/", response_model=ArticleRestType)
async def create_new_article(options: ArticleOptionsRestType = Body(embed=True),
                             current_user: UserModel = Depends(get_current_active_user)):
    new_article = ArticleModel()
    new_article.set_from_rest_type(options)
    new_article.author = current_user

    db.session.add(new_article)
    db.session.commit()
    return new_article.rest_type()


@router.put("/{article_id}", response_model=ArticleRestType)
async def update_article(article_id: int,
                         options: ArticleOptionsRestType = Body(embed=True),
                         current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(article_id)

    if article.author != current_user and not current_user.is_admin:
        raise HTTPException(status_code=401, detail="you have no permission to edit this article")

    article.set_from_rest_type(options)
    db.session.commit()

    return article.rest_type()
