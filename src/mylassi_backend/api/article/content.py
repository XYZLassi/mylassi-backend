from typing import List

from fastapi import Depends, Body, Request, HTTPException
from sqlalchemy.orm import Session

from mylassi_data.db import get_db
from mylassi_data.restschema import *
from . import router
from .__fn__ import get_article_or_404

from mylassi_data.models import *
from ..security import get_current_active_user


@router.get("/{article}/content", response_model=List[ArticleContentRestType],
            operation_id='getContentsFromArticle')
async def get_all_contents_from_article(article: ArticleModel = Depends(get_article_or_404(True))) \
        -> List[ArticleContentRestType]:
    return [c.rest_type() for c in article.contents]


@router.get("/{article}/content/{content}", response_model=ArticleContentRestType,
            operation_id='getContentFromArticle')
async def get_article_content(content: int,
                              article: ArticleModel = Depends(get_article_or_404(True)),
                              session: Session = Depends(get_db)) \
        -> ArticleContentRestType:
    content: ArticleContentModel = ArticleContentModel.get_or_404(session, content)

    assert content in article.contents

    return content.rest_type()


@router.post("/{article}/content/{content}", response_model=ArticleContentRestType,
             operation_id='updateArticleContent')
async def update_article_content(content: int,
                                 article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                                 options: ArticleContentOptionsRestType = Body(embed=False),
                                 current_user: UserModel = Depends(get_current_active_user),
                                 session: Session = Depends(get_db)) \
        -> ArticleContentRestType:
    content: ArticleContentModel = ArticleContentModel.get_or_404(session, content)

    assert content in article.contents

    content.set_from_rest_type(options)
    session.commit()

    return content.rest_type()


@router.post("/{article}/content/", response_model=List[ArticleContentRestType],
             operation_id='addArticleContent', name='Add Contents To article')
@router.put("/{article}/content/", response_model=List[ArticleContentRestType],
            operation_id='replaceContent', name='Replace Contents To Article')
async def add_replace_article_content(request: Request,
                                      article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                                      options: List[ArticleContentOptionsRestType] = Body(embed=False),
                                      session: Session = Depends(get_db)) \
        -> List[ArticleContentRestType]:
    results: List[ArticleContentModel] = list()

    if request.method == 'PUT':
        for old_content in article.contents:
            session.delete(old_content)
        article.contents.clear()

    for option in options:
        content_model = ArticleContentModel()
        content_model.set_from_rest_type(option)

        article.contents.append(content_model)
        results.append(content_model)

    session.commit()

    return [c.rest_type() for c in results]


@router.delete("/{article}/content/{content}", response_model=OkayResultRestType,
               operation_id='deleteContent')
async def remove_article_content(content: int,
                                 article: ArticleModel = Depends(get_article_or_404(True, test_owner=True)),
                                 session: Session = Depends(get_db)) \
        -> OkayResultRestType:
    content: ArticleContentModel = ArticleContentModel.get_or_404(session, content)

    assert content in article.contents

    article.contents.remove(content)
    # noinspection PyUnresolvedReferences
    article.contents.reorder()
    session.delete(content)
    session.commit()

    return OkayResultRestType(okay=True)
