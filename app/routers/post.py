from fastapi import Response, HTTPException, Depends, APIRouter
from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas
from ..database import get_db
from .. import oauth2

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# GET
@router.get("/", response_model=List[schemas.ResponsePostGet])
async def test_posts(db: Session = Depends(get_db), limit: int = 20, skip: int = 0, search: Optional[str] = ""):
    # res = db.query(models.Post).order_by(models.Post.created_at).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    res = await db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.created_at).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    
    if not res:
        raise HTTPException(status_code=404, detail="no post available!")
    return res

@router.get("/latest", response_model=List[schemas.ResponsePostGet])
def get_latest_post(db: Session=Depends(get_db), limit: int = 10, skip: int = 0):
    res = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).order_by(models.Post.created_at.desc()).limit(limit).offset(skip).all()
    
    if not res:
        raise HTTPException(status_code=404, detail="no posts available!")
    return res

@router.get("/{id}", response_model=schemas.ResponsePostGet)
def get_post(id: int, db: Session=Depends(get_db)):
    res = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not res:
        raise HTTPException(status_code=404, detail=f"post with id={id} doesn't exist!")
    return res

# POSTS
@router.post("/", status_code=201, response_model=schemas.ResponsePostBase)
def create_post(post: schemas.RequestPostCreate, db: Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    try:
        res = models.Post(user_id=current_user.id, **post.dict())
        db.add(res)
        db.commit()
        db.refresh(res)
    except:
        raise HTTPException(status_code=403, detail="not authorized to post!")
    
    return res

#DELETE
@router.delete("/", status_code=204)
def delete_all(db: Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    res = db.query(models.Post)
    current_user_posts = res.filter(models.Post.user_id == current_user.id)
    
    if not res.first():
        raise HTTPException(status_code=404, detail="no post available!")
    
    elif not current_user_posts.first():
        raise HTTPException(status_code=404, detail="no post available for current user!")
    
    current_user_posts.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)

@router.delete("/{id}", status_code=204)
def delete_post(id: int, db: Session=Depends(get_db), current_user = Depends(oauth2.get_current_user)):
    res = db.query(models.Post).filter(models.Post.id == id)
    
    if not res.first():
        raise HTTPException(status_code=404, detail=F"post with id={id} doesn't exist!")
    
    elif not res.first().user_id == current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to delete this post!")
    
    res.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=204)
    
#UPDATE
@router.put("/{id}", status_code=200, response_model=schemas.ResponsePostUpdate)
def update_post(id: int, new_post: schemas.RequestPostUpdate, db: Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == id)
    
    if not post.first():
        raise HTTPException(status_code=404, detail=f"post with id={id} doesn't exist!")
    
    elif not post.first().user_id == current_user.id:
        raise HTTPException(status_code=403, detail="not authorized to update this post!")
    
    post.update(new_post.dict(), synchronize_session=False)
    db.commit()
    
    res = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    return res