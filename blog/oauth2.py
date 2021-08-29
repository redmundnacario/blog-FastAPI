from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from . import token, schemas, models, database
import json

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_user(email: str, db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(models.User.email == email).first()
    return user

def get_current_user(data: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    email = token.verify_token(data, credentials_exception)
    print (email)
    current_user = get_user(email, db)
    print (current_user)
    if not current_user:
        raise credentials_exception

    return current_user.__dict__