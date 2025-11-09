from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List

from .database import Base

class User(Base):
    __tablename__ = 'users'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), index=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    posts: Mapped[List['Post']] = relationship('Post', 
                                            back_populates='author',
                                            foreign_keys='Post.author_id') 
    
class Post(Base):
    __tablename__ = 'posts'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), default='')
    published_date: Mapped[date] = mapped_column(default=date.today)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    author: Mapped['User'] = relationship(back_populates='posts') # back_populates - обратное отношение к модели User
#     tags: Mapped[List['Tag']] = relationship(secondary=post_tag_association, back_populates='posts')
#     comments: Mapped[List['Comment']] = relationship(secondary=post_tag_association, back_populates='posts')
    
# class Comment(Base):
#     # ...
#     posts: Mapped[List['Post']] = relationship(secondary=post_tag_association, back_populates='comments')
    
# class Tag(Base):
#     # ...
#     posts: Mapped[List['Post']] = relationship(secondary=post_tag_association, back_populates='tags')