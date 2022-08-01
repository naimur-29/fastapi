from pydantic import BaseModel
from typing import Optional
from datetime import datetime

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
    
    class Config:
        orm_mode = True