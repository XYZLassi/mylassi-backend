from typing import List

from fastapi import Depends, Body
from sqlalchemy.orm import Session

from mylassi_data.db import get_db
from mylassi_data.models import *
from mylassi_data.restschema import *
from . import router
from .__fn__ import get_article_or_404
from ..file import upload_file


@router.get('/{article}/files', response_model=List[ArticleFileRestType],
            operation_id='getArticleFiles')
async def get_article_files(article: ArticleModel = Depends(get_article_or_404(True))):
    return [fa.rest_type() for fa in article.file_associations]


@router.get('/{article}/files/{article_file}', response_model=ArticleFileRestType)
async def get_article_file(article_file: int,
                           article: ArticleModel = Depends(get_article_or_404(True)),
                           session: Session = Depends(get_db)):
    article_file = ArticleFileModel.get_or_404(session, article_file)
    assert article_file in article.file_associations

    return article_file.rest_type()


@router.post('/{article}/uploadFile', response_model=ArticleFileRestType,
             operation_id='uploadFileToArticle')
async def upload_file_to_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                                 file_id: str = Depends(upload_file()),
                                 session: Session = Depends(get_db)):
    try:
        article_file = ArticleFileModel()
        article_file.file_id = file_id

        article.file_associations.append(article_file)
        session.commit()
    except:
        # Todo: delete File
        raise

    return article_file.rest_type()


@router.post('/{article}/files', response_model=List[ArticleFileRestType],
             operation_id='addFileToArticle')
async def add_files_to_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                               options: List[AppendArticleFileOptionsRestType] = Body(embed=False),
                               session: Session = Depends(get_db)):
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
async def add_or_replace_files_to_article(article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                                          options: List[AppendArticleFileOptionsRestType] = Body(embed=False),
                                          session: Session = Depends(get_db)):
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
async def update_article_file(article_file: int,
                              article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                              options: ArticleFileOptionsRestType = Body(embed=False),
                              session: Session = Depends(get_db), ):
    article_file = ArticleFileModel.get_or_404(session, article_file)

    assert article_file in article.file_associations
    article_file.set_from_rest_type(options)
    session.commit()
    return article_file.rest_type()
