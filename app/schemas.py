from pydantic import BaseModel
from typing import Optional


class UserModel(BaseModel):
    user: str
    email: str
    password: str

    
class UserResponse(BaseModel):
    id: int
    user: str
    email: str
    password: str
    
    class Config:
        from_attributes=True

class TokenData(BaseModel):
    id : Optional[int] = None