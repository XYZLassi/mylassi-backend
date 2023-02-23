__all__ = ['router']

from operator import and_
from typing import List, Union

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from mylassi_data.db import get_db
from mylassi_data.models import *
from mylassi_data.restschema import *
from .file import upload_file
from .security import get_current_active_user

router = APIRouter(tags=['Articles'], prefix='/articles')


@router.get("/", response_model=List[ArticleRestType],
            operation_id='getArticles')
async def get_articles(category: int = None,
                       session: Session = Depends(get_db)):
    query = ArticleModel.q(session)

    query = query.filter(ArticleModel.is_deleted == False)

    if category is not None:
        query = query.filter(ArticleModel.categories.any(CategoryModel.id == category))

    return [p.rest_type() for p in query.all()]


@router.get("/all", response_model=List[FullArticleRestType],
            operation_id='getAllArticles')
async def get_all_articles(category: int = None,
                           session: Session = Depends(get_db),
                           current_user: UserModel = Depends(get_current_active_user)):
    query = ArticleModel.q(session)

    if not current_user.is_admin:
        query = query.filter_by(author_id=current_user.id)

    if category is not None:
        query = query.filter(ArticleModel.categories.any(CategoryModel.id == category))

    return [p.full_rest_type() for p in query.all()]


@router.get("/{article}", response_model=ArticleRestType,
            operation_id='getArticle')
async def get_article(article: int,
                      session: Session = Depends(get_db)):
    article = ArticleModel.get_or_404(session, article)

    return article.rest_type()


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


@router.put("/{article}", response_model=ArticleRestType,
            operation_id='updateArticle')
async def update_article(article: int,
                         options: ArticleOptionsRestType = Body(embed=False),
                         session: Session = Depends(get_db),
                         current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(session, article)

    if article.author != current_user and not current_user.is_admin:
        raise HTTPException(status_code=401, detail="you have no permission to edit this article")

    article.set_from_rest_type(options)
    session.commit()

    return article.rest_type()


@router.delete('/{article}', response_model=OkayResultRestType,
               operation_id='deleteArticle')
async def delete_article(article: int,
                         session: Session = Depends(get_db),
                         current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(session, article)

    if article.author != current_user and not current_user.is_admin:
        raise HTTPException(status_code=401, detail="you have no permission to edit this article")

    article.is_deleted = True
    session.commit()
    return OkayResultRestType(okay=True)


@router.post('/{article}/restore', response_model=FullArticleRestType,
             operation_id='restoreArticle')
async def restore_article(article: int,
                          session: Session = Depends(get_db),
                          current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(session, article)

    if article.author != current_user and not current_user.is_admin:
        raise HTTPException(status_code=404, detail="Item not found")

    article.is_deleted = False
    session.commit()
    return article.full_rest_type()


@router.post('/{article}/category', response_model=ArticleRestType,
             operation_id='addCategoryToArticle')
async def add_category_to_article(article: int,
                                  categories: Union[int, List[int]] = Body(embed=True),
                                  session: Session = Depends(get_db),
                                  current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(session, article)

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
async def replace_category_to_article(article: int,
                                      categories: Union[int, List[int]] = Body(embed=False),
                                      session: Session = Depends(get_db),
                                      current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(session, article)

    if isinstance(categories, int):
        categories = [categories]

    article.clear_categories()

    selected_categories = CategoryModel.q(session) \
        .filter(CategoryModel.id.in_(categories))
    selected_categories = selected_categories.all()

    article.append_categories(*selected_categories)

    session.commit()

    return article.rest_type()


@router.post('/{article}/uploadFile', response_model=ArticleFileRestType,
             operation_id='uploadFileToArticle')
async def upload_file_to_article(article: int,
                                 file_id: str = Depends(upload_file()),
                                 session: Session = Depends(get_db),
                                 current_user: UserModel = Depends(get_current_active_user)):
    try:
        article = ArticleModel.get_or_404(session, article)

        article_file = ArticleFileModel()
        article_file.file_id = file_id

        article.file_associations.append(article_file)
        session.commit()
    except:
        # Todo: delete File
        raise

    return article_file.rest_type()


@router.get('/{article}/files', response_model=List[ArticleFileRestType],
            operation_id='getArticleFiles')
async def get_article_files(article: int,
                            session: Session = Depends(get_db)):
    article = ArticleModel.get_or_404(session, article)

    return [fa.rest_type() for fa in article.file_associations]


@router.put('/{article}/files/{article_file}', response_model=ArticleFileRestType,
            operation_id='updateArticleFile')
async def update_article_file(article: int, article_file: int,
                              options: ArticleFileOptionsRestType = Body(embed=False),
                              session: Session = Depends(get_db),
                              current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(session, article)
    article_file = ArticleFileModel.get_or_404(session, article_file)

    assert article_file in article.file_associations
    article_file.set_from_rest_type(options)
    session.commit()
    return article_file.rest_type()
