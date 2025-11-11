from pydantic import BaseModel
from typing import List
from typing_extensions import Self
from datetime import date

from typing import Optional
    
class Post(BaseModel):
    id: int
    title: str
    content: str

class PostIn(BaseModel):
    title: str
    content: str
    author_id: int
    
class PostOut(BaseModel):
    id: int
    title: str
    content: str
    author_id: int
    # author: str
    publish_date: date
    
    class Config:
        from_attributes = True