from fastapi import Response, HTTPException, Depends, APIRouter
from typing import List
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)

# GET
@router.get("/", response_model=List[schemas.ResponseUserGet])
def get_users(db: Session=Depends(get_db)):
    res = db.query(models.User).order_by(models.User.created_at).all()
    
    if not res:
        raise HTTPException(status_code=404, detail="no user available!")
    return res

@router.get('/{id}', response_model=schemas.ResponseUserGet)
def get_user_by_id(id: int, db: Session=Depends(get_db)):
    res = db.query(models.User).filter(models.User.id == id).first()
    
    if not res:
        raise HTTPException(status_code=404, detail=f"user with {id} doesn't exist!")
    return res

@router.get('/{id}/posts', response_model=List[schemas.ResponsePostGet])
def get_posts_by_user_id(id: int, db: Session=Depends(get_db)):
    res = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.user_id == id).all()
    
    if not res:
        user = db.query(models.User).filter(models.User.id == id).first()
        if not user:
            raise HTTPException(status_code=404, detail=f"user with id:{id} doesn't exist!")
        
        raise HTTPException(status_code=404, detail=f"user {id} doesn't have any posts!")
    
    return res

# POST
@router.post("/", status_code=201, response_model=schemas.ResponseUserCreate)
def create_user(user: schemas.RequestUserCreate, db: Session=Depends(get_db)):
    # HASH THE PASSWORD
    user.password = utils.hash(user.password)
    res = models.User(**user.dict())
    
    try:
        db.add(res)
        db.commit()
        db.refresh(res)
        return res
    except:
        raise HTTPException(status_code=409, detail="user already exists!")