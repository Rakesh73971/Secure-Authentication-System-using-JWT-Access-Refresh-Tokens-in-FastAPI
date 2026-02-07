from fastapi.security import OAuth2PasswordBearer
from .config import settings
from .schemas import TokenData
from sqlalchemy.orm import Session
from . import database,models
from fastapi import Depends,HTTPException,status
from jose import jwt,JWTError
from datetime import datetime,timedelta

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY=settings.secret_key
ALGORITHM=settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES=settings.access_token_expire_minutes
REFRESH_TOKEN_EXPIRE_DAYS=settings.refresh_token_expire_days

def create_access_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({'exp':expire,'type':'access'})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def create_refresh_token(data:dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({'exp':expire,'type':'refresh'})
    encode_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encode_jwt

def verify_access_token(token:str):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get('type') != 'access':
            raise HTTPException(status_code=401,detail='Invalid access token')
        user_id:int = payload.get('user_id')
        if user_id is None:
            raise HTTPException(status_code=401,detail='Invalid token')
        return TokenData(id=user_id)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"}
        )


def verify_refresh_token(token):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        if payload.get('type') != 'refresh':
            raise HTTPException(status_code=401,detail='Invalid refresh token')
        user_id = payload.get('user_id')
        if user_id is None:
            raise HTTPException(status_code=401,detail='Invalid refresh token')
        return user_id
    except JWTError:
        raise HTTPException(status_code=401,detail='Invalid refresh token')
    
def get_current_user(token:str=Depends(oauth_scheme),db:Session=Depends(database.get_db)):
    token_data = verify_access_token(token)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if user is None:
        raise HTTPException(status_code=404,detail='user not found')
    return user