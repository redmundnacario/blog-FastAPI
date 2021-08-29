from fastapi import FastAPI
from blog import models
from blog.database import engine
from blog.routers import blogs, users, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)


app.include_router(authentication.router)
app.include_router(blogs.router)
app.include_router(users.router)