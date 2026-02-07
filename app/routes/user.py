from fastapi import APIRouter,Depends
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils
from typing import List

router = APIRouter(
    prefix='/users',
    tags=['User']
)

@router.get('/',response_model=List[schemas.UserResponse])
def get_users(db:Session=Depends(get_db)):
    users = db.query(models.User).all()
    return users

@router.post('/',response_model=schemas.UserResponse)
def create_user(user_data:schemas.UserModel,db:Session=Depends(get_db)):
    hashed_password = utils.hashed(user_data.password)
    user_data.password = hashed_password
    db_user = models.User(**user_data.dict())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user