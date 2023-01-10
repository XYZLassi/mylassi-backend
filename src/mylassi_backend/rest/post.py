__all__ = ['router']

from typing import List

from fastapi import APIRouter, Body, Depends, HTTPException

from mylassi_data.restschema import *
from mylassi_data.models import *

from mylassi_data import db

from .security import get_current_active_user

router = APIRouter(tags=['Posts'])


@router.get("/posts/", response_model=List[PostRestType])
async def get_posts():
    return [p.rest_type() for p in PostModel.all()]


@router.post("/posts/", response_model=PostRestType)
async def create_new_post(options: PostOptionsRestType = Body(embed=True),
                          current_user: UserModel = Depends(get_current_active_user)):
    new_post = PostModel()
    new_post.set_from_rest_type(options)
    new_post.author = current_user

    db.session.add(new_post)
    db.session.commit()
    return new_post.rest_type()


@router.put("/posts/{post_id}", response_model=PostRestType)
async def update_post(post_id: int,
                      options: PostOptionsRestType = Body(embed=True),
                      current_user: UserModel = Depends(get_current_active_user)):
    post = PostModel.get_or_404(post_id)

    if post.author != current_user and not current_user.is_admin:
        raise HTTPException(status_code=401, detail="you have no permission to edit this post")

    post.set_from_rest_type(options)
    db.session.commit()

    return post.rest_type()
