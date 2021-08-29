from fastapi import FastAPI
from . import models
from .database import engine
from .routers import blogs, users, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(blogs.router)
app.include_router(users.router)