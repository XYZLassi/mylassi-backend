__all__ = [
    'router',
    'oauth2_scheme',
    'encode_auth_token', 'decode_auth_token',
    'get_current_user', 'get_current_active_user',
]

import datetime
import os

import jwt
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from starlette import status

from mylassi_data.db import get_db
from mylassi_data.models import *
from mylassi_data.restschema import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'My-Secret-Key')
ALGORITHM = os.environ.get('ALGORITHM', "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/token/docs")

router = APIRouter(tags=['Security'])


def encode_auth_token(user_id, minutes_to_expire: int = ACCESS_TOKEN_EXPIRE_MINUTES,
                      **kwargs):
    try:
        exp: datetime.timedelta = datetime.timedelta(minutes=minutes_to_expire)
        payload = {
            'exp': datetime.datetime.utcnow() + exp,
            'iat': datetime.datetime.utcnow(),
            'sub': user_id
        }
        payload.update(**kwargs)

        return jwt.encode(
            payload,
            SECRET_KEY,
            algorithm=ALGORITHM
        )
    except Exception as e:
        raise e


def decode_auth_token(auth_token):
    try:
        payload = jwt.decode(auth_token, SECRET_KEY, algorithms=ALGORITHM)
        return payload
    except jwt.ExpiredSignatureError:
        raise
    except jwt.InvalidTokenError:
        raise


async def get_current_user(token: str = Depends(oauth2_scheme),
                           session: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_auth_token(token)
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except:
        raise credentials_exception
    user = UserModel.get(session, user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=TokenRestType,
             operation_id='createNewToken')
@router.post("/token/docs", include_in_schema=False)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 expire_time: int = ACCESS_TOKEN_EXPIRE_MINUTES,
                                 session: Session = Depends(get_db)):
    user = UserModel.get_by_username(session, form_data.username)

    assert expire_time > 0

    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = encode_auth_token(user.id, minutes_to_expire=expire_time)
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/token/refresh/", response_model=TokenRestType,
             operation_id='refreshToken')
async def refresh_token(expire_time: int = ACCESS_TOKEN_EXPIRE_MINUTES,
                        current_user: UserModel = Depends(get_current_active_user)):
    access_token = encode_auth_token(current_user.id, minutes_to_expire=expire_time)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserRestType,
            operation_id='me')
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user.rest_type(all_data=True)
