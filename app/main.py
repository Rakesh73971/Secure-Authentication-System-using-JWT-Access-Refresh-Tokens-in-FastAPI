from fastapi import FastAPI
from .routes import user
from . import models
from .database import engine

models.Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(user.router)