from fastapi import APIRouter, HTTPException, status
from fastapi.param_functions import Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from typing import Annotated
from datetime import timedelta

from config.database import db
from utils.hash import Hash
from models.tokenModel import Token
from auth.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token

user_collection = db.get_collection("users")

async def authenticate_user(username: str, password: str):
    user = await user_collection.find_one({"username": username})

    if user is None:
        return False
    
    if not Hash.verify(password, user['password']):
        return False
    
    return user

router = APIRouter(
    tags=['auth']
)

@router.post('/token')
async def get_token(
    form_data: Annotated[OAuth2PasswordRequestForm,  Depends()]
) -> Token:
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": str(user['_id'])}, expires_delta=access_token_expires
    )

    return Token(access_token=access_token, token_type="bearer")

