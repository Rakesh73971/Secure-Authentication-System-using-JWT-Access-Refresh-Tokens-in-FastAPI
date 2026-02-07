from fastapi import APIRouter,Depends
from ..oauth2 import get_current_user
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models

router = APIRouter(
    prefix='/user',
    tags=['User']
)

@router.get('/')
def get_posts(db:Session=Depends(get_db),user=Depends(get_current_user)):
    posts = db.query(models.User).all()
    return posts