from fastapi.security import OAuth2PasswordRequestForm
from fastapi import APIRouter,Depends,HTTPException
from sqlalchemy.orm import Session
from .. import database,models,utils
from ..schemas import RefreshTokenRequest
from ..oauth2 import create_access_token,create_refresh_token,verify_refresh_token


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username
    ).first()

    if not user or not utils.verify(
        user_credentials.password, user.password
    ):
        raise HTTPException(status_code=403, detail="Invalid credentials")

    access_token = create_access_token({"user_id": user.id})
    refresh_token = create_refresh_token({"user_id": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh_token(request: RefreshTokenRequest):
    user_id = verify_refresh_token(request.refresh_token)

    new_access_token = create_access_token({"user_id": user_id})

    return {
        "access_token": new_access_token,
        "token_type": "bearer"
    }