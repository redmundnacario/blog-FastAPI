from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from blog import database, models, schemas, oauth2
from blog.hashing import Hash
from blog.controllers import users


router = APIRouter(
    prefix = "/user",
    tags = ["Users"]
)

get_db = database.get_db


@router.get("/current", response_model=schemas.UserSecured)
async def get_current_user(current_user: schemas.User = Depends(oauth2.get_current_user)):
    return current_user

@router.get("/{id}/blogs", status_code = 200, response_model = schemas.UserShow)
def get_user(id: int, db: Session = Depends(get_db),
             current_user: schemas.User = Depends(oauth2.get_current_user)
):
    return users.get(id, db)