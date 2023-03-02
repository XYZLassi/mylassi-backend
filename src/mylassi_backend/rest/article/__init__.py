__all__ = ['router']

from fastapi import APIRouter

router = APIRouter(tags=['Articles'], prefix='/articles')

from . import base
from . import file
from . import category
