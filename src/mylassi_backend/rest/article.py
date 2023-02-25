__all__ = ['router']

from operator import and_
from typing import List, Union, Optional

from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.orm import Session

from mylassi_data.db import get_db
from mylassi_data.models import *
from mylassi_data.restschema import *
from mylassi_tools.pagination import decode_cursor, encode_cursor
from .file import upload_file
from .security import get_current_active_user

router = APIRouter(tags=['Articles'], prefix='/articles')


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

    query = query.limit(size)

    items = query.all()

    return PaginationResultRestType[ArticleRestType](
        items=[p.rest_type() for p in items],
        cursor=encode_cursor(items[-1].id) if len(items) > 0 else None,
        size=size,
    )


@router.get("/all", response_model=PaginationResultRestType[FullArticleRestType],
            operation_id='getAllArticles')
async def get_all_articles(category: Optional[int] = None,
                           cursor: Optional[str] = None, size: int = 5,
                           session: Session = Depends(get_db),
                           current_user: UserModel = Depends(get_current_active_user)) \
        -> PaginationResultRestType[FullArticleRestType]:
    query = ArticleModel.q(session)
    query = query.order_by(ArticleModel.id.desc())

    if not current_user.is_admin:
        query = query.filter_by(author_id=current_user.id)

    if category is not None:
        query = query.filter(ArticleModel.categories.any(CategoryModel.id == category))

    if cursor and (cursor_id := decode_cursor(cursor)):
        query = query.filter(ArticleModel.id < cursor_id)

    query = query.limit(size)

    items = query.all()

    return PaginationResultRestType[FullArticleRestType](
        items=[p.full_rest_type() for p in items],
        cursor=encode_cursor(items[-1].id) if len(items) > 0 else None,
        size=size,
    )


@router.get("/{article}", response_model=ArticleRestType,
            operation_id='getArticle')
async def get_article(article: int,
                      session: Session = Depends(get_db)) -> ArticleRestType:
    article = ArticleModel.get_or_404(session, article)

    return article.rest_type()


@router.get("/{article}/full", response_model=FullArticleRestType,
            operation_id='getFullArticle')
async def get_full_article(article: int,
                           session: Session = Depends(get_db),
                           current_user: UserModel = Depends(get_current_active_user)) -> FullArticleRestType:
    article = ArticleModel.get_or_404(session, article)

    if article.author != current_user and not current_user.is_admin:
        raise HTTPException(status_code=404, detail="Item not found")

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
                                  categories: Union[int, List[int]] = Body(embed=True),  # Todo: List
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
                                      categories: Union[int, List[int]] = Body(embed=False),  # Todo: List
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


@router.post('/{article}/files', response_model=List[ArticleFileRestType],
             operation_id='addFileToArticle')
async def add_files_to_article(article: int,
                               options: List[AppendArticleFileOptionsRestType] = Body(embed=False),
                               session: Session = Depends(get_db),
                               current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(session, article)

    results = list()
    for option in options:
        article_file_model = ArticleFileModel.first(session, article_id=article.id, file_id=option.file_id)

        if not article_file_model:
            article_file_model = ArticleFileModel()
            article_file_model.file_id = option.file_id
            article_file_model.article_id = article.id
            session.add(article_file_model)

        article_file_model.set_from_rest_type(option)
        results.append(article_file_model)
    session.commit()

    return [r.rest_type() for r in results]


@router.put('/{article}/files', response_model=List[ArticleFileRestType],
            operation_id='addOrReplaceFilesToArticle')
async def add_or_replace_files_to_article(article: int,
                                          options: List[AppendArticleFileOptionsRestType] = Body(embed=False),
                                          session: Session = Depends(get_db),
                                          current_user: UserModel = Depends(get_current_active_user)):
    article = ArticleModel.get_or_404(session, article)

    old_files = list(article.file_associations)

    results = list()
    for option in options:
        article_file_model = ArticleFileModel.first(session, article_id=article.id, file_id=option.file_id)

        if not article_file_model:
            article_file_model = ArticleFileModel()
            article_file_model.file_id = option.file_id
            article_file_model.article_id = article.id
            session.add(article_file_model)
        else:
            old_files.remove(article_file_model)

        article_file_model.set_from_rest_type(option)
        results.append(article_file_model)

    for old_file in old_files:
        session.delete(old_file)

    session.commit()

    return [r.rest_type() for r in results]


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
