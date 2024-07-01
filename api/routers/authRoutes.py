from starlette.config import Config
from fastapi import APIRouter, HTTPException, status, Depends, Body
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import Annotated
from datetime import timedelta, datetime, timezone
from auth.oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES, jwt

from config.database import db
from utils.hash import Hash
from models.tokenModel import Token, RefeshToken
from models.loginModel import Login

user_collection = db.get_collection("users")

router = APIRouter(
    tags=['auth']
)

config = Config('.env')
ALGORITHM = "HS256"
refresh_token_expire_minutes = 60 * 24 * 7

async def authenticate_user(username: str, password: str):
    user = await user_collection.find_one({"username": username})

    if user is None:
        return False
    
    if not Hash.verify(password, user['password']):
        return False
    
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    data_to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data_to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(data_to_encode, config('SECRET'), algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: dict):
    data_to_encode = data.copy()
    expire = timedelta(minutes=refresh_token_expire_minutes) + datetime.utcnow()
    data_to_encode.update({"exp": expire})
    refesh_token = jwt.encode(data_to_encode, config('SECRET'), algorithm=ALGORITHM)

    return refesh_token

def verify_refesh_token(token: str):
    credential_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}        
    )

    try:
        payload = jwt.decode(token, config('SECRET'), algorithm=ALGORITHM)
    except:
        raise credential_exception

    id: str = payload.get("id")

    if id is None:
        raise credential_exception

    return id

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

@router.post('/login')
async def login(login: Login):
    if login.username == None or login.password == None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    user = await authenticate_user(login.username, login.password)
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"id": str(user['_id'])}, expires_delta=access_token_expires
    )

    refresh_token = create_refresh_token(
        data={"id": str(user['_id'])}
    )

    return { 'access_token': access_token, 'refresh_token': refresh_token }

@router.post('/refresh')
def refesh(token: RefeshToken = Body(...)):
    user_id = verify_refesh_token(token.refesh_token)

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"id": str(user_id)}, expires_delta=access_token_expires
    ) 

    return { 'access_token': access_token }