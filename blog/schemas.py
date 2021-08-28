from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    content : str

class BlogShow(Blog):
    class Config:
        orm_mode = True

class BlogPatch(BaseModel):
    title: Optional[str]
    content: Optional[str]


class User(BaseModel):
    username: str
    email: str
    password: str

class UserShow(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True