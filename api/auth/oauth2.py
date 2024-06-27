from fastapi.security import OAuth2PasswordBearer
from typing import Optional
from datetime import datetime, timedelta, timezone
import jwt
#from jose import jwt
from jwt.exceptions import InvalidTokenError
from typing import Annotated
from fastapi.param_functions import Depends
from fastapi import HTTPException, status

from config.database import db
from models.userModel import UserModel, UserCollection

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')
user_collection = db.get_collection("users")

SECRET_KEY = 'f2357ede086afd4eceeb9a27f0f69b44a7786516e8700ebabc1843d312b0cfa8'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 30
 
def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
      expire = datetime.now(timezone.utc) + expires_delta
  else:
      expire = datetime.now(timezone.utc) + timedelta(minutes=15)
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
  return encoded_jwt

async def get_current_user(token: Annotated[str, Depends(oauth2_schema)]):
  credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail='Unable to validate credentials',
    headers={"WWW-Authenticate": "Bearer"},
  )

  try:
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    username: str = payload.get('sub')
  except InvalidTokenError:
    raise credentials_exception
  
  user = await user_collection.find_one({"username": username})

  if user is None:
    raise credentials_exception
  
  return user