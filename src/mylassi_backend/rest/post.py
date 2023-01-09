__all__ = ['router']

from typing import List

from fastapi import APIRouter, Body, Depends

from mylassi_data.restschema import *
from mylassi_data.models import *

from mylassi_data import db

from .security import get_current_active_user, oauth2_scheme

router = APIRouter(tags=['Posts'])


@router.get("/posts/", response_model=List[PostRestType])
async def get_posts():
    return [p.rest_type() for p in PostModel.all()]


@router.post("/posts/", response_model=PostRestType)
async def create_new_post(create_options: CreateNewPostRestType = Body(embed=True),
                          current_user: UserModel = Depends(get_current_active_user)):
    new_post = PostModel()

    new_post.title = create_options.title
    new_post.content = create_options.content
    new_post.author = current_user

    db.session.add(new_post)
    db.session.commit()
    return new_post.rest_type()
