from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

# adding cors
origins = [
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
    
)

posts_db = [
    {
        "id": 0,
        "title": "post title",
        "content": "post details...",
        "published": False,
        "rating": 3
    },
    {
        "id": 1,
        "title": "post title",
        "content": "post details...",
        "published": False,
        "rating": 3
    },
    {
        "id": 2,
        "title": "post title",
        "content": "post details...",
        "published": False,
        "rating": 3
    }
]

class Post(BaseModel):
    id: Optional[int] = None
    title: str
    content: str
    published: bool = False
    rating: Optional[int] = None

# GET
@app.get("/")
async def root():
    return {"message": "hello world!"}

@app.get("/posts")
def get_posts():
    if not posts_db:
        raise HTTPException(status_code=404, detail="no post available!")
    return {"data": posts_db}

@app.get("/posts/latest")
def get_latest_post():
    try: return {"data": posts_db[len(posts_db)-1]}
    except:
        raise HTTPException(status_code=404, detail="no post available!")

@app.get("/posts/{id}")
def get_post(id: int):
    try: return {f"post no.{id}": posts_db[id]}
    except: raise HTTPException(status_code=404, detail=f"{id} doesn't exist!")
    
# POSTS
@app.post("/posts", status_code=201)
def create_post(post: Post):
    post.id = len(posts_db)
    posts_db.append(post.dict())
    print(posts_db)
    return {"data": post}

#DELETE
@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int):
    try:
        posts_db.pop(id)
        return Response(status_code=204)
    except:
        raise HTTPException(status_code=404, detail=f"post:{id} doesn't exist!")
    
#UPDATE
@app.put("/posts/{id}", status_code=200)
def update_post(id: int, post: Post):
    post.id = id
    try:
        posts_db[id] = post.dict()
        return {"updated post": post}
    except:
        raise HTTPException(status_code=404, detail=f"post:{id} doesn't exist!")