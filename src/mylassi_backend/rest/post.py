__all__ = ['router']

from typing import List

from fastapi import APIRouter

import mylassi_backend.rest.models as api_models
from mylassi_data.models.post import Post

router = APIRouter(tags=['Posts'])


@router.get("/posts/", response_model=List[api_models.Post])
async def get_posts():
    def get_return():
        for post in Post.all():
            yield api_models.Post(
                id=post.id,
                title=post.title,
                author=f'/author/{post.author_id}'
            )

    return list(get_return())
