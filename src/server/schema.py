from datetime import date, datetime
from numpy import str
from pydantic import BaseModel, EmailStr
from typing import Optional

import uuid

class UserInfo(BaseModel):
    username: Optional[str]
    password: Optional[str]
    email: EmailStr
    company: str
    place: str
    phone: str

class UserIn(BaseModel):
    username: str
    password: Optional[str]

class UserOut(BaseModel):
    username: str
    email: EmailStr
    company: str
    place: str
    phone: str
    class Config():
        orm_mode =True

class UserBoardInfo(BaseModel):
    user: str
    board: str

class UserBoardOut(BaseModel):
    id: uuid.UUID
    board_name: str
    is_favorite: bool
    is_latest_read: bool
    last_post: date

class BoardInfo(BaseModel):
    board: str

class PostInfo(BaseModel):
    post_id: uuid.UUID
    author: str
    board: str
    title: str
    article: str
    like: Optional[int]
    hate: Optional[int]
    post_datetime: datetime

class PostOut(BaseModel):
    author: str
    board_name: str
    title: str
    article: str
    like: Optional[int]
    post_date: date
    favor: Optional[str]

class PostGuide(BaseModel):
    id: uuid.UUID
    author: str
    post_date: date
    title: str
    like: int    
    is_read: bool
    
class WritePost(BaseModel):
    board_id: Optional[uuid.UUID]
    board_name: Optional[str]
    title: str
    content: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    user_id: uuid.UUID
    username: str
    email: EmailStr
    company: str
    place: str
    phone: str
    