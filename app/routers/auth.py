from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..database import get_db
from .. import models, utils, oauth2, schemas

router = APIRouter(
    tags=["Authentication"]
)

@router.post("/login", response_model=schemas.ResponseToken)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(), db: Session=Depends(get_db)):
    res = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if not res:
        raise HTTPException(status_code=403, detail="Invalid Credentials!")
    
    elif not utils.verify(user_credentials.password, res.password):
        raise HTTPException(status_code=403, detail="Invalid Credentials!")
    
    # CREATE TOKEN
    access_token = oauth2.create_access_token(data = {"user_id": res.id})
    
    return {"access_token": access_token, "token_type": "Bearer"}