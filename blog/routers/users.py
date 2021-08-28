from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from .. import database, models, schemas
from ..hashing import Hash
from ..controllers import users

router = APIRouter(
    prefix = "/user",
    tags = ["Users"]
)

get_db = database.get_db


@router.post("/", status_code = status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return users.create(request, db)


@router.get("/{id}", status_code = 200, response_model = schemas.UserShow)
def get_user(id: int, db: Session = Depends(get_db)):
    return users.get(id, db)