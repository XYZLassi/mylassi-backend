from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from mylassi_data.db import get_db
from mylassi_data.restschema import *
from mylassi_data.models import *

router = APIRouter(tags=['Authors'])


@router.get("/authors/", response_model=List[AuthorRestType])
async def get_authors(session: Session = Depends(get_db)):
    return [u.rest_type_author() for u in UserModel.q(session).filter(UserModel.article_count > 0).all()]
