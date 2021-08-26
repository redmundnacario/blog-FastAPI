from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from . import models, schemas
from .schemas import Blog
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(engine)

@app.post("/blog")
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, content=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog