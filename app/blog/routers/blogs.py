from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from typing import List
from blog import database, schemas, oauth2
from blog.controllers import blogs


router = APIRouter(
    tags = ["Blogs"]
)


get_db = database.get_db


@router.get("/blogs", status_code=200, response_model = List[schemas.BlogShow])
def get_all_blogs(db: Session = Depends(get_db),
                  current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return blogs.get_all(db)


@router.post("/blog",status_code=status.HTTP_201_CREATED)
def create_blog(request: schemas.Blog, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return blogs.create(request, db)


@router.get("/blog/{id}", status_code=200, response_model = schemas.BlogShow)
def get_blog(id: int, db: Session = Depends(get_db),
             current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return blogs.get(id, db)


@router.put("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db),
                current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return blogs.update(id, request, db)


@router.patch("/blog/{id}", status_code=status.HTTP_202_ACCEPTED)
def edit_blog(id: int, request: schemas.BlogPatch, 
              db: Session = Depends(get_db),
              current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return blogs.edit(id, request, db)


@router.delete("/blog/{id}")
def destroy_blog(id: int, db: Session = Depends(get_db),
                 current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return blogs.destroy(id, db)
