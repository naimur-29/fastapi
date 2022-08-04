from fastapi import FastAPI, Response, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, oauth2, models

router = APIRouter(
    prefix="/vote",
    tags=["Votes"]
)

@router.post("/{id}", status_code=201)
def vote(id: int, db: Session=Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    res = db.query(models.Vote).filter(models.Vote.post_id == id, models.Vote.user_id == current_user.id)
        
    if res.first():
        res.delete(synchronize_session=False)
        db.commit()
        
        return {"message": "removed the vote!"}
    
    new_vote = models.Vote(post_id=id, user_id=current_user.id)
    try:
        db.add(new_vote)
        db.commit()
    except:
        raise HTTPException(status_code=404, detail=f"post {id} doesn't exist!")
    
    return {"message": "successfully added a vote!"}