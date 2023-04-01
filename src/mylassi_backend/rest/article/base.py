from typing import Optional

from fastapi import Body, Depends, HTTPException
from sqlalchemy.orm import Session

from mylassi_data.db import get_db
from mylassi_data.models import *
from mylassi_data.restschema import *
from mylassi_tools.pagination import decode_cursor, encode_cursor

from ..security import get_current_active_user
from ..filters import *

from . import router
from .__fn__ import *


@router.get("/", response_model=PaginationResultRestType[ArticleRestType],
            operation_id='getArticles')
async def get_articles(category: int = None,
                       cursor: Optional[str] = None, size: int = 5,
                       session: Session = Depends(get_db)) \
        -> PaginationResultRestType[ArticleRestType]:
    if size <= 0 or size > 50:
        size = 5

    query = ArticleModel.q(session)
    query = query.order_by(ArticleModel.id.desc())
    query = query.filter(ArticleModel.is_deleted_flag == None)

    if category is not None:
        query = query.filter(ArticleModel.categories.any(CategoryModel.id == category))

    if cursor and (cursor_id := decode_cursor(cursor)):
        query = query.filter(ArticleModel.id < cursor_id)

    query_count = query.count()
    query = query.limit(size)

    items = query.all()

    return PaginationResultRestType[ArticleRestType](
        items=[p.rest_type() for p in items],
        cursor=encode_cursor(items[-1].id) if len(items) > 0 and query_count > size else None,
        pageSize=size,
        length=len(items)
    )


@router.get("/all", response_model=PaginationResultRestType[FullArticleRestType],
            operation_id='getAllArticles')
async def get_all_articles(category: Optional[int] = None,
                           cursor: Optional[str] = None, size: int = 5,
                           filter_deleted: FilterDeletedItems = FilterDeletedItems.only_not_deleted_items,
                           session: Session = Depends(get_db),
                           current_user: UserModel = Depends(get_current_active_user)) \
        -> PaginationResultRestType[FullArticleRestType]:
    query = ArticleModel.q(session)
    query = query.order_by(ArticleModel.id.desc())

    if not current_user.is_admin:
        query = query.filter_by(author_id=current_user.id)

    if category is not None:
        query = query.filter(ArticleModel.categories.any(CategoryModel.id == category))

    if filter_deleted == FilterDeletedItems.only_not_deleted_items:
        query = query.filter(ArticleModel.is_deleted == False)
    elif filter_deleted == FilterDeletedItems.only_deleted_items:
        query = query.filter(ArticleModel.is_deleted == True)

    if cursor and (cursor_id := decode_cursor(cursor)):
        query = query.filter(ArticleModel.id < cursor_id)

    query_count = query.count()
    query = query.limit(size)

    items = query.all()

    return PaginationResultRestType[FullArticleRestType](
        items=[p.full_rest_type() for p in items],
        cursor=encode_cursor(items[-1].id) if len(items) > 0 and query_count > size else None,
        pageSize=size,
        length=len(items)
    )


@router.get("/{article}", response_model=ArticleRestType,
            operation_id='getArticle')
async def get_article(article: ArticleModel = Depends(get_article_or_404(True))) -> ArticleRestType:
    return article.rest_type()


@router.get("/{article}/full", response_model=FullArticleRestType,
            operation_id='getFullArticle')
async def get_full_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True))) \
        -> FullArticleRestType:
    return article.full_rest_type()


@router.post("/", response_model=ArticleRestType,
             operation_id='createNewArticle')
async def create_new_article(
        options: ArticleOptionsRestType = Body(embed=False),
        session: Session = Depends(get_db),
        current_user: UserModel = Depends(get_current_active_user)):
    new_article = ArticleModel()
    new_article.set_from_rest_type(options)
    new_article.author = current_user

    session.add(new_article)
    session.commit()
    return new_article.rest_type()


@router.put("/{article}", response_model=FullArticleRestType,
            operation_id='updateArticle')
async def update_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                         options: ArticleOptionsRestType = Body(embed=False),
                         session: Session = Depends(get_db)):
    article = ArticleModel.get_or_404(session, article)

    article.set_from_rest_type(options)
    session.commit()
    return article.full_rest_type()


@router.delete('/{article}', response_model=OkayResultRestType,
               operation_id='deleteArticle')
async def delete_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                         session: Session = Depends(get_db)):
    article.is_deleted = True
    session.commit()
    return OkayResultRestType(okay=True)


@router.post('/{article}/restore', response_model=FullArticleRestType,
             operation_id='restoreArticle')
async def restore_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                          session: Session = Depends(get_db), ):
    article = ArticleModel.get_or_404(session, article)

    article.is_deleted = False
    session.commit()
    return article.full_rest_type()
