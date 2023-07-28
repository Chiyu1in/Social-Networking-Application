import uuid

from fastapi import status, HTTPException

from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database.models import User, Board, Post, UserBoards, UserPosts


def query_user_from_id(id: uuid.UUID, db: Session):

    return db.query(User).filter(User.user_id==id)


def query_user_from_name(name: str, db: Session):

    return db.query(User).filter(User.username==name)


def query_board_from_id(id: uuid.UUID, db: Session):

    return db.query(Board).filter(Board.board_id==id)


def query_board_from_name(name: str, db: Session):

    return db.query(Board).filter(Board.board_name==name)

def query_post_from_id(id: uuid.UUID, db: Session):

    return db.query(Post).filter(Post.post_id==id)


def query_userboard(user_id: uuid.UUID, db: Session):

    return db.query(UserBoards).filter(UserBoards.user_id==user_id)


