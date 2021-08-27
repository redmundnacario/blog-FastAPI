from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

app = FastAPI()


# get all blogs
@app.get("/blog")
def index(limit:int = 10,
          published:bool = True,
          sort:Optional[str] = None):
    if published:
        return {"data":{
            "content" : ["blog1", "blog2"],
            "limit" : limit,
            "published" : published,
            "sort" : sort
        }}
    else:
        return {"data":{
            "content" : ["blog1", "blog2"],
            "limit" : limit,
            "published" : published,
            "sort" : sort
        }}

# get all unpublished blogs
@app.get("/blog/unpublished")
def get_unpublished_blogs(limit:int = 10,
                          sort:Optional[str] = None):
    return {"data":{
            "content" : ["blog1", "blog2"],
            "limit" : limit,
            "published" : False,
            "sort" : sort
        }}

# get all comments within the blog
@app.get("/blog/{id}/comments")
def get_comments(id:int,
                 limit:int = 10):
    return {"data": {
        "blog_id" : id,
        "limit" : limit,
        "comments" : ["comment 1", "comment 2"]}
    }

class Blog(BaseModel):
    title : str
    content : str
    published : Optional[bool]



# post: create a blog
@app.post('/blog')
def create_blog(request: Blog):
    return {"data": f"Created a blog with title as {request.title}"}

# if __name__ == "__main__":
#     uvicorn.run(app, host="0.0.0.0", port=8000)