from typing import List

from fastapi import APIRouter, Body, Depends

from mylassi_backend.rest.security import get_current_active_user
from mylassi_data import db
from mylassi_data.models import CategoryModel, UserModel
from mylassi_data.restschema import *

router = APIRouter(tags=['Categories'], prefix='/categories')


@router.get("/", response_model=List[CategoryRestType])
async def get_categories():
    return [c.rest_type() for c in CategoryModel.all()]


@router.get("/{category}", response_model=CategoryRestType)
async def get_category(category: int):
    return CategoryModel.get_or_404(category).rest_type()


@router.post("/", response_model=CategoryRestType)
async def create_category(options: CategoryOptionRestType = Body(embed=True),
                          current_user: UserModel = Depends(get_current_active_user)):
    new_category = CategoryModel()
    new_category.set_from_rest_type(options)

    db.session.add(new_category)
    db.session.commit()

    return new_category.rest_type()


@router.put("/{category}", response_model=CategoryRestType)
async def update_category(category: int,
                          options: CategoryOptionRestType = Body(embed=True),
                          current_user: UserModel = Depends(get_current_active_user)):
    category = CategoryModel.get_or_404(category)
    category.set_from_rest_type(options)

    db.session.commit()

    return category.rest_type()
