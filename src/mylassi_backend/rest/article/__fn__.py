__all__ = ['get_article_or_404']

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from mylassi_backend.rest.security import get_current_active_user
from mylassi_data.db import get_db
from mylassi_data.models import *


def get_article_or_404(check_deleted: bool, test_owner: bool = False):
    error_404_text = 'article not found'

    async def helper_get_404(article: int, session: Session = Depends(get_db)) -> ArticleModel:
        article = ArticleModel.get_or_404(session, article, error_text=error_404_text)

        if check_deleted and article.is_deleted:
            raise HTTPException(status_code=404, detail=error_404_text)

        return article

    async def helper_get_404_test_owner(article: ArticleModel = Depends(helper_get_404),
                                        current_user: UserModel = Depends(get_current_active_user)):
        if article.author != current_user and not current_user.is_admin:
            raise HTTPException(status_code=404, detail=error_404_text)

        return article

    if test_owner:
        return helper_get_404_test_owner
    return helper_get_404
