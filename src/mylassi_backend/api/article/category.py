from operator import and_
from typing import Union, List

from fastapi import Body, Depends
from sqlalchemy.orm import Session

from mylassi_data.db import get_db
from mylassi_data.models import *
from mylassi_data.restschema import *
from . import router
from .__fn__ import *


@router.post('/{article}/category', response_model=ArticleRestType,
             operation_id='addCategoryToArticle')
async def add_category_to_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                                  categories: Union[int, List[int]] = Body(embed=True),  # Todo: List
                                  session: Session = Depends(get_db), ):
    if isinstance(categories, int):
        categories = [categories]

    already_category_id = [c.article_file_id for c in article.categories]
    selected_categories = CategoryModel.q(session) \
        .filter(and_(CategoryModel.id.in_(categories), CategoryModel.id.not_in(already_category_id)))
    selected_categories = selected_categories.all()

    article.append_categories(*selected_categories)

    session.commit()

    return article.rest_type()


@router.put('/{article}/category', response_model=ArticleRestType,
            operation_id='replaceCategoryToArticle')
async def replace_category_to_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                                      categories: Union[int, List[int]] = Body(embed=False),  # Todo: List
                                      session: Session = Depends(get_db)):
    if isinstance(categories, int):
        categories = [categories]

    article.clear_categories()

    selected_categories = CategoryModel.q(session) \
        .filter(CategoryModel.id.in_(categories))
    selected_categories = selected_categories.all()

    article.append_categories(*selected_categories)

    session.commit()

    return article.rest_type()
