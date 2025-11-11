from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import date
from typing import List

from app.db.models.base import Base
from app.db.models.annotations import intpk

class Post(Base):
    __tablename__ = 'posts'
    
    id: Mapped[intpk] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    content: Mapped[str] = mapped_column(String(1000), default='')
    published_date: Mapped[date] = mapped_column(default=date.today)
    author_id: Mapped[int] = mapped_column(ForeignKey('users.id', ondelete='CASCADE'))
    author: Mapped['User'] = relationship(back_populates='posts') # back_populates - обратное отношение к модели User
#     tags: Mapped[List['Tag']] = relationship(secondary=post_tag_association, back_populates='posts')
#     comments: Mapped[List['Comment']] = relationship(secondary=post_tag_association, back_populates='posts')
    
# class Comment(Base):
#     # ...
#     posts: Mapped[List['Post']] = relationship(secondary=post_tag_association, back_populates='comments')
    
# class Tag(Base):
#     # ...
#     posts: Mapped[List['Post']] = relationship(secondary=post_tag_association, back_populates='tags')