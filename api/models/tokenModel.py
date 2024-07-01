from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str

class RefeshToken(BaseModel):
    refesh_token: str