from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List

from app.db.models.base import Base
from app.db.models.annotations import intpk

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[intpk] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    posts: Mapped[List['Post']] = relationship('Post', 
                                            back_populates='author',
                                            foreign_keys='Post.author_id') 
    