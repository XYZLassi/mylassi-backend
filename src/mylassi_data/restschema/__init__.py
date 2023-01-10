__all__ = [
    'TokenRestType',
    'UserRestType',
    'AuthorRestType',
    'PostRestType', 'CreateNewPostRestType',
]

from .token import TokenRestType
from .user import UserRestType
from .post import PostRestType, CreateNewPostRestType
from .author import AuthorRestType
