import os
import motor.motor_asyncio
from starlette.config import Config

if os.getenv("ENV") is 'prod':
    db = os.getenv("DB")
else:
    config = Config('.env')
    db = config('DB')

client = motor.motor_asyncio.AsyncIOMotorClient(db)

db = client.apisec