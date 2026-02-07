from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    name: str
    email: str
    password: str

    
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    
    class Config:
        from_attributes=True

class TokenData(BaseModel):
    id : Optional[int] = None

class RefreshTokenRequest(BaseModel):
    refresh_token: str