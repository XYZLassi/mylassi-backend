from typing import List

from fastapi import APIRouter

from mylassi_data.restschema import *
from mylassi_data.models import *

router = APIRouter(tags=['Authors'])


@router.get("/authors/", response_model=List[AuthorRestType])
async def get_authors():
    return [u.rest_type_author() for u in UserModel.q().filter(UserModel.post_count > 0).all()]
