from pydantic import BaseModel
from typing import Optional

class Blog(BaseModel):
    title: str
    content : str

class ShowBlog(Blog):
    class Config:
        orm_mode = True

class BlogPatch(BaseModel):
    title: Optional[str]
    content: Optional[str]