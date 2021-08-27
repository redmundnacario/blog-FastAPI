from fastapi import FastAPI, Depends, status, Response, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas
from .schemas import Blog
from .database import engine, get_db

app = FastAPI()

models.Base.metadata.create_all(engine)


@app.get(
            "/blog", 
            status_code=200,
            response_model = List[schemas.ShowBlog]
            )
def get_all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.post(
            "/blog",
            status_code=status.HTTP_201_CREATED
            )
def create_blog(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title = request.title, content=request.content)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get(
        "/blog/{id}", 
        status_code=200,
        response_model = schemas.ShowBlog
        )
def get_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "error": f"Blog with id of {id} is not available."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Blog with id of {id} was not found."
            )
    return blog


@app.put(
        "/blog/{id}", 
        status_code=status.HTTP_202_ACCEPTED
        )
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Blog with id of {id} was not found." 
        )

    blog.update(request.dict())
    db.commit()
    return request
    # return blog.first()


@app.patch(
        "/blog/{id}", 
        status_code=status.HTTP_202_ACCEPTED
        )
def edit_blog(id: int, request: schemas.BlogPatch, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Blog with id of {id} was not found." 
        )
    
    old_data = { key : blog.first().__dict__[key] for key in request.dict().keys()}
    update_data = {**old_data, **request.dict(exclude_unset=True)}
    
    blog.update(update_data)
    db.commit()
    return update_data


@app.delete(    
            "/blog/{id}"
            )
def destroy_blog(id: int, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Blog with id of {id} was not found." 
        )
    blog.delete(synchronize_session=False)
    db.commit()
    # return "done"
    return Response(status_code=status.HTTP_204_NO_CONTENT)

