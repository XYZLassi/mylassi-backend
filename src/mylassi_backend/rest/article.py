__all__ = ['router']

from operator import and_
from typing import List, Union

from fastapi import APIRouter, Body, Depends, HTTPException

from mylassi_data import db
from mylassi_data.models import *
from mylassi_data.restschema import *
from .security import get_current_active_user

router = APIRouter(tags=['Articles'], prefix='/articles')


@router.get("/", response_model=List[ArticleRestType])
async def get_articles(category: int = None):
    query = ArticleModel.q()

    if category is not None:
        query = query.filter(ArticleModel.categories.any(CategoryModel.id == category))

    return [p.rest_type() for p in query.all()]


@router.post("/", response_model=ArticleRestType)
async def create_new_article(options: ArticleOptionsRestType = Body(embed=True),
                             current_user: UserModel = Depends(get_current_active_user)):
    new_article = ArticleModel()
    new_article.set_from_rest_type(options)
    new_article.author = current_user

    db.session.add(new_article)
    db.session.commit()
    return new_article.rest_type()


@router.put("/{article}", response_model=ArticleRestType)
async def update_article(article: int,
                         options: ArticleOptionsRestType = Body(embed=True),
                         current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(article)

    if article.author != current_user and not current_user.is_admin:
        raise HTTPException(status_code=401, detail="you have no permission to edit this article")

    article.set_from_rest_type(options)
    db.session.commit()

    return article.rest_type()


@router.post('/{article}/category', response_model=ArticleRestType)
async def add_category_to_article(article: int, categories: Union[int, List[int]] = Body(embed=True)):
    article = ArticleModel.get_or_404(article)
    already_category_id = [c.id for c in article.categories]

    if isinstance(categories, int):
        categories = [categories]

    selected_categories = CategoryModel.q() \
        .filter(and_(CategoryModel.id.in_(categories), CategoryModel.id.not_in(already_category_id)))
    selected_categories = selected_categories.all()

    for cat in selected_categories:
        article.categories.append(cat)

    db.session.commit()

    return article.rest_type()
