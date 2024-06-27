from fastapi import APIRouter, status, Body
from models.sensitiveModel import SensitiveData
from cryptography.fernet import Fernet
from starlette.config import Config

router = APIRouter(
    tags=['sensitive']
)

config = Config('.env')
key = config('KEY')
fernet = Fernet(key)

@router.post(
    '/sensitivedata',
    status_code=status.HTTP_201_CREATED,
)
async def post_encrypted(Data: SensitiveData = Body(...)):
    encrypted_data = fernet.encrypt(Data.unencrypted_data.encode())

    print(fernet.decrypt(encrypted_data).decode())
    
    return { 'encrypted_data': encrypted_data }