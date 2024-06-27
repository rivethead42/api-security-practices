from fastapi import APIRouter, status, Body, HTTPException, Depends
from pydantic.functional_validators import BeforeValidator
from typing_extensions import Annotated
from bson import ObjectId
from pymongo import ReturnDocument
import nh3

from models.userModel import UserModel, UserCollection
from config.database import db
from auth.oauth2 import oauth2_schema
from utils.hash import Hash

user_collection = db.get_collection("users")
PyObjectId = Annotated[str, BeforeValidator(str)]

router = APIRouter(
    tags=['user']
)

@router.get(
    '/users',
    summary='Returns a list of users in JSON format with no authorization.',
    description='Returns a list of users in JSON format.',
    response_model=UserCollection
    )
async def get_users(token: str = Depends(oauth2_schema)):
    return UserCollection(users=await user_collection.find().to_list(1000))

@router.get(
    '/noauth/users',
    summary='Returns a list of users in JSON format.',
    description='Returns a list of users in JSON format.',
    response_model=UserCollection
    )
async def get_users():
    return UserCollection(users=await user_collection.find().to_list(1000))

@router.get(
    '/users/{id}', 
    status_code=status.HTTP_200_OK,
    summary='Returns a user by id in JSON format.',
    description='Returns a user by id in JSON format.',
    response_model=UserModel
    )
async def get_user(id: str, token: str = Depends(oauth2_schema)):
    if (
        user := await user_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return user
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {id} not found')

@router.post(
    '/users',
    status_code=status.HTTP_201_CREATED,
    response_model=UserModel
)
async def post_user(User: UserModel = Body(...)):
    User.password = Hash.bcrypt(User.password)
    User.firstname = nh3.clean(User.firstname)
    User.lastname = nh3.clean(User.lastname)
    User.username = nh3.clean(User.username)
    User.email = nh3.clean(User.email)

    new_user = await user_collection.insert_one(
        User.model_dump(by_alias=True)
    )

    created_user = await user_collection.find_one(
        {"_id": new_user.inserted_id}
    )
    return created_user

@router.put(
    '/users{id}',
    response_model=UserModel
)
async def post_user( id: str, User: UserModel = Body(...), token: str = Depends(oauth2_schema)):
    user = {
        k: v for k, v in User.model_dump(by_alias=True).items() if v is not None
    }

    if len(user) >= 1:
        update_user = await user_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": user},
            return_document=ReturnDocument.AFTER,
        )

        if update_user is not None:
            return update_user
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User {id} not found')