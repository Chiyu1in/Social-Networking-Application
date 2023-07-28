import re

from sqlalchemy import BIGINT, Column, BigInteger, Boolean, \
                        Date, DateTime, Enum, Float, ForeignKey, Integer, \
                        String, UniqueConstraint, and_, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base, relationship
from database.utils import get_engine_from_pgconfig
#from utils import get_engine_from_pgconfig


Base = declarative_base()
engine = get_engine_from_pgconfig()

class User(Base):
    __tablename__ = 'Users'
    user_id = Column(UUID(True), primary_key=True)
    username = Column(String(), unique=True, nullable=False)
    password = Column(String(), nullable=False)
    company = Column(String(), nullable=False)
    place = Column(String(), nullable=False)
    email = Column(String(), nullable=False)
    phone = Column(String(), nullable=False)
    
    post = relationship("Post", back_populates="author")    
    user_boards = relationship("UserBoards", back_populates="user")
    user_posts = relationship("UserPosts", back_populates="user")

class Board(Base):
    __tablename__ = 'Boards'
    board_id = Column(UUID(True), primary_key=True)
    board_name = Column(String(), unique=True, nullable=False)

    post = relationship("Post", back_populates="board")
    user_boards = relationship("UserBoards", back_populates="board")
       
class Post(Base):
    __tablename__ = 'Posts'
    post_id = Column(UUID(True), primary_key=True)
    title = Column(String(), nullable=False)
    content = Column(String(), nullable=False)
    author_id = Column(UUID(True), ForeignKey(User.user_id), nullable=False)
    like = Column(Integer(), nullable=False)
    hate = Column(Integer(), nullable=False)
    post_time = Column(DateTime(), nullable=False)
    board_id =  Column(UUID(True), ForeignKey(Board.board_id), nullable=False)

    author = relationship("User", back_populates="post")
    board = relationship("Board", back_populates="post")
    user_posts = relationship("UserPosts", back_populates="post")

class UserBoards(Base):
    __tablename__ = 'UserBoards'
    id = Column(BigInteger(), primary_key=True)
    user_id = Column(UUID(True), ForeignKey(User.user_id), nullable=False)
    board_id = Column(UUID(True), ForeignKey(Board.board_id), nullable=False)
    is_favorite = Column(Boolean(), nullable=False)
    is_latest_read = Column(Boolean(), nullable=False)
    last_post = Column(DateTime(), nullable=False)
    
    user = relationship("User", back_populates="user_boards")
    board = relationship("Board", back_populates="user_boards")

class UserPosts(Base):
    __tablename__ = 'UserPosts'
    id = Column(BigInteger(), primary_key=True)
    user_id = Column(UUID(True), ForeignKey(User.user_id), nullable=False)
    post_id = Column(UUID(True), ForeignKey(Post.post_id), nullable=False)
    is_read = Column(Boolean(), nullable=False)
    favor = Column(String())

    user = relationship("User", back_populates="user_posts")
    post = relationship("Post", back_populates="user_posts")


def create_table():
    Base.metadata.create_all(engine)