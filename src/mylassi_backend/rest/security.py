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

from dotenv import load_dotenv
from starlette import status

from mylassi_data.restschema import *

from mylassi_data.models import *

load_dotenv('.env')

SECRET_KEY = os.environ['SECRET_KEY']
ALGORITHM = os.environ.get('ALGORITHM', "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter(tags=['Security'])


def encode_auth_token(user_id,
                      exp: datetime.timedelta = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
                      **kwargs):
    try:
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


async def get_current_user(token: str = Depends(oauth2_scheme)):
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
    user = UserModel.get(user_id)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserModel = Depends(get_current_user)) -> UserModel:
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/token", response_model=TokenRestType)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = UserModel.get_by_username(form_data.username)

    if not user or not user.check_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = encode_auth_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserRestType)
async def read_users_me(current_user: UserModel = Depends(get_current_active_user)):
    return current_user.rest_type(all_data=True)
