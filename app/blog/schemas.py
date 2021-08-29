from pydantic import BaseModel
from typing import Optional, List


class User(BaseModel):
    username: str
    email: str
    password: str

class UserSecured(BaseModel):
    username: str
    email: str

class BlogBase(BaseModel):
    title: str
    content : str

class Blog(BlogBase):
    class Config:
        orm_mode = True



class UserShow(BaseModel):
    username: str
    blogs: List[Blog] = []
    class Config:
        orm_mode = True

class UserShowLimited(BaseModel):
    username: str
    class Config:
        orm_mode = True



class BlogShow(BlogBase):
    author: UserShowLimited
    class Config:
        orm_mode = True

class BlogPatch(BaseModel):
    title: Optional[str]
    content: Optional[str]



class Login(BaseModel):
    email : str
    password : str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None