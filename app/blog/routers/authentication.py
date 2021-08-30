from fastapi import APIRouter, status, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from blog import schemas, models
from blog.database import get_db
from blog.hashing import Hash
from blog.token import create_access_token,\
                       ACCESS_TOKEN_EXPIRE_MINUTES
from blog import oauth2
from blog.controllers import users



router = APIRouter(
    tags = ["Authentication"]
)

@router.post("/login", response_model= schemas.Token)
# def login(data: schemas.Login, db: Session = Depends(get_db)):
def login(data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == data.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password."
        )

    if not Hash.verify(data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect username or password."
        )

    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/signup", status_code = status.HTTP_201_CREATED)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    return users.create(request, db)


