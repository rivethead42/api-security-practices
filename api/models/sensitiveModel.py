from pydantic import BaseModel

class SensitiveData(BaseModel):
    unencrypted_data: str