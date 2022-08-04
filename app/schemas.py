from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional
from pydantic.types import conint

#USER
class RequestUserCreate(BaseModel):
    email: EmailStr
    password: str
    
class ResponseUserCreate(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class ResponseUserGet(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    
    class Config:
        orm_mode = True
        
class ResponseUserInPost(BaseModel):
    id: int
    email: EmailStr
    
    class Config:
        orm_mode = True

# POST
class RequestPostBase(BaseModel):
    title: str
    content: str
    published: bool = True

class RequestPostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    
class RequestPostUpdate(BaseModel):
    title: str
    content: str
    published: bool = True

class ResponsePostBase(BaseModel):
    id: int
    title: str
    content: str
    published: bool
    created_at: datetime
    user: ResponseUserInPost
    
    class Config:
        orm_mode = True
        
class ResponsePostGet(BaseModel):
    Post: ResponsePostBase
    votes: int
        
class ResponsePostUpdate(ResponsePostGet):
    pass
    
#AUTHENTICATION
class ResponseToken(BaseModel):
    access_token: str
    token_type: str
    
class RequestTokenData(BaseModel):
    id: Optional[str]