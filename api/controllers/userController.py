from models.userModel import UserModel, UserCollection
from config.database import db
from typing_extensions import Annotated
from pydantic.functional_validators import BeforeValidator
from bson import ObjectId
from utils.hash import Hash

PyObjectId = Annotated[str, BeforeValidator(str)]

user_collection = db.get_collection("users")

async def get_users() -> UserCollection:
    return UserCollection(users=await user_collection.find().to_list(1000))

async def authenticate_user(username: str, password: str):
    print(username)
    user = await user_collection.find_one({"_id": ObjectId(username)})

    print(user)

    if user is None:
        return False
    
    if not Hash.verify(password, user.password):
        return False
    
    return user