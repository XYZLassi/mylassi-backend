__all__ = ['router']

from typing import List

from fastapi import APIRouter

from mylassi_data.restschema import *
from mylassi_data.models import *

router = APIRouter(tags=['Posts'])


@router.get("/posts/", response_model=List[PostRestType])
async def get_posts():
    def get_return():
        for post in PostModel.all():
            yield PostRestType(
                id=post.id,
                title=post.title,
                author=f'/author/{post.author_id}'
            )

    return list(get_return())
