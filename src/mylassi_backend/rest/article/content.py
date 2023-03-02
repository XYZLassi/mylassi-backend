from typing import List

from fastapi import Depends, Body, Request, HTTPException
from sqlalchemy.orm import Session

from mylassi_data.db import get_db
from mylassi_data.restschema import *
from . import router

from mylassi_data.models import *
from ..security import get_current_active_user


@router.get("/{article}/content/{content}", response_model=ArticleContentRestType,
            operation_id='getArticleContent')
def get_article_content(article: int, content: int, session: Session = Depends(get_db)) \
        -> ArticleContentRestType:
    article: ArticleModel = ArticleModel.get_or_404(session, article)
    content: ArticleContentModel = ArticleContentModel.get_or_404(session, content)

    assert content in article

    return content.rest_type()


@router.post("/{article}/content/", response_model=List[ArticleContentRestType],
             operation_id='addArticleContent', name='Add contents to article')
@router.put("/{article}/content/", response_model=List[ArticleContentRestType],
            operation_id='replaceArticleContent', name='Replace contents to article')
def add_replace_article_content(article: int, request: Request,
                                options: List[ArticleContentOptionsRestType] = Body(embed=False),
                                session: Session = Depends(get_db),
                                current_user: UserModel = Depends(get_current_active_user)) \
        -> List[ArticleContentRestType]:
    article: ArticleModel = ArticleModel.get_or_404(session, article)

    if article.author != current_user and not current_user.is_admin:
        raise HTTPException(status_code=404, detail="Item not found")

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
