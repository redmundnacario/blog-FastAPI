from fastapi import status, HTTPException, Response
from sqlalchemy.orm import Session
from .. import models, schemas


def get_all(db: Session):
    blogs = db.query(models.Blog).all()
    return blogs


def create(request: schemas.Blog, db: Session):
    new_blog = models.Blog(
        title= request.title,
        content= request.content,
        author_id = 1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


def get(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return { "error": f"Blog with id of {id} is not available."}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Blog with id of {id} was not found."
            )
    return blog


def update(id: int, request: schemas.Blog, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)

    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Blog with id of {id} was not found." 
        )

    blog.update(request.dict())
    db.commit()
    return request


def edit(id: int, request: schemas.BlogPatch, db: Session):
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


def destroy(id: int, db: Session):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail = f"Blog with id of {id} was not found." 
        )
    blog.delete(synchronize_session=False)
    db.commit()
    # return "done"
    return Response(status_code=status.HTTP_204_NO_CONTENT)