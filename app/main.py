from fastapi import FastAPI, Response, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
# import psycopg2
# from  psycopg2.extras import RealDictCursor
import time
from typing import Optional, List
from sqlalchemy.orm import Session
from . import models
from .database import engine, get_db
from . import schemas;

models.Base.metadata.create_all(bind=engine)

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

# CONNECTION TO THE DATABASE USING DEFAULT DRIVER
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres', password='whatwentwrong', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print("db connection successful...")
#         break
#     except Exception as error:
#         print("db connection failed!")
#         print(error)
#         time.sleep(2)

# GET
@app.get("/")
def root():
    return {"message": "add '/docs' after the url to get the documentations!"}

#USING DEFAULT DRIVER
# @app.get("/posts")
# def get_posts():
#     cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC;""")
#     res = cursor.fetchall()
    
#     if not res:
#         raise HTTPException(status_code=404, detail="no post available!")
#     else: 
#         return {"posts": res}

# @app.get("/posts/latest")
# def get_latest_post():
#     cursor.execute("""SELECT * FROM posts ORDER BY created_at DESC LIMIT 1;""")
#     res = cursor.fetchone()
    
#     if not res:
#         raise HTTPException(status_code=404, detail="no posts available!")
#     else:
#         return {"latest post": res}

# @app.get("/posts/{id}")
# def get_post(id: int):
#     cursor.execute("""SELECT * FROM posts WHERE id = %s;""", (str(id)))
#     res = cursor.fetchone()
    
#     if not res:
#         raise HTTPException(status_code=404, detail=f"post with id={id} doesn't exist!")
#     else:
#         return {f"post with id={id}": res}

#USING ORM SQL ALCHEMY
@app.get('/posts', response_model=List[schemas.ResponsePostBase])
def test_posts(db: Session = Depends(get_db)):
    res = db.query(models.Post).order_by(models.Post.created_at).all()
    
    if not res:
        raise HTTPException(status_code=404, detail="no post available!")
    return res

@app.get("/posts/latest", response_model=schemas.ResponsePostBase)
def get_latest_post(db: Session=Depends(get_db)):
    res = db.query(models.Post).order_by(models.Post.created_at.desc()).first()
    
    if not res:
        raise HTTPException(status_code=404, detail="no posts available!")
    return res

@app.get("/posts/{id}", response_model=schemas.ResponsePostBase)
def get_post(id: int, db: Session=Depends(get_db)):
    res = db.query(models.Post).filter(models.Post.id == id).first()
    
    if not res:
        raise HTTPException(status_code=404, detail=f"post with id={id} doesn't exist!")
    return res

# POSTS
# USING DEFAULT DRIVER
# @app.post("/posts", status_code=201)
# def create_post(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *;""", (post.title, post.content, post.published))
#     res = cursor.fetchone()
#     conn.commit()
    
#     return {"post created successfully": res}

#USING ORM
@app.post("/posts", status_code=201, response_model=schemas.ResponsePostBase)
def create_post(post: schemas.RequestPostCreate, db: Session=Depends(get_db)):
    res = models.Post(**post.dict())
    db.add(res)
    db.commit()
    db.refresh(res)
    
    return res

#DELETE
#USING DEFAULT DRIVER
# @app.delete("/posts/{id}", status_code=204)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *;""", (str(id)))
#     res = cursor.fetchone()
#     conn.commit()
    
#     if not res:
#         raise HTTPException(status_code=404, detail=F"post with id={id} doesn't exist!")
#     else:
#         return Response(status_code=204)

#USING ORM
@app.delete("/posts/all", status_code=204)
def delete_all(db: Session=Depends(get_db)):
    res = db.query(models.Post)
    
    if not res.first():
        raise HTTPException(status_code=404, detail="no post available!")
    res.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

@app.delete("/posts/{id}", status_code=204)
def delete_post(id: int, db: Session=Depends(get_db)):
    res = db.query(models.Post).filter(models.Post.id == id)
    
    if not res.first():
        raise HTTPException(status_code=404, detail=F"post with id={id} doesn't exist!")
    res.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)
    
#UPDATE
#USING DEFAULT DRIVER
# @app.put("/posts/{id}", status_code=200)
# def update_post(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *;""", (post.title, post.content, post.published, str(id)))
#     res = cursor.fetchone()
#     conn.commit()
    
#     if not res:
#         raise HTTPException(status_code=404, detail=f"post with id={id} doesn't exist!")
#     else:
#         return {"updated post": res}

#USING ORM
@app.put("/posts/{id}", status_code=200, response_model=schemas.ResponsePostBase)
def update_post(id: int, post: schemas.RequestPostUpdate, db: Session=Depends(get_db)):
    res = db.query(models.Post).filter(models.Post.id == id)
    
    if not res.first():
        raise HTTPException(status_code=404, detail=f"post with id={id} doesn't exist!")
    res.update(post.dict(), synchronize_session=False)
    db.commit()
    return res.first()