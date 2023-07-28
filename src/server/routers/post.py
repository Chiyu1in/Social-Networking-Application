import uuid
from datetime import datetime, timezone, timedelta
from fastapi import APIRouter, Depends, status

from sqlalchemy import desc
from sqlalchemy.orm import Session
from database.utils import get_db
from database.models import User, Board, Post, UserBoards, UserPosts
# from database.method import query_post_id, query_user_name, query_board_name

from schema import PostOut, WritePost, TokenData, PostGuide
from oauth2 import get_current_user

router = APIRouter(
    tags=['Posts']
)

@router.get("/posts/")
async def get_posts_in_board(board_id: uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
     
    posts = (
        db.query(Post, User.username.label('author')).join(User)
        .filter(Post.board_id==board_id)
        .order_by(desc(Post.post_time)) 
        .all())

    read_posts = get_read_posts(board_id, db, current_user)
    read_posts = { read_post.post_id for read_post in read_posts }

    posts = [
        PostGuide(
            id = post.Post.post_id,
            title = post.Post.title,
            author = post.author,
            like = post.Post.like-post.Post.hate,
            post_date = post.Post.post_time.date(),
            is_read = (post.Post.post_id in read_posts)
        )
        for post in posts]

    return posts
    

@router.get("/post/{id}/", response_model=PostOut)
async def get_post(id: uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    
    post = (db.query(Post, User.username.label('author'), Board.board_name.label('board_name'))
        .join(User).join(Board).filter(Post.post_id==id).first())

    post = PostOut(
        author = post.author,
        board_name = post.board_name,
        title = post.Post.title,
        article = post.Post.content,
        like = post.Post.like-post.Post.hate,
        post_date = post.Post.post_time.date()
    )

    user_post = (db.query(UserPosts).filter(UserPosts.user_id==current_user.user_id, 
        UserPosts.post_id==id).first())
    if user_post: post.favor = user_post.favor

    return post


@router.put("/post/{id}/read/")
async def read_post(id:uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    
    query = db.query(UserPosts).filter(UserPosts.user_id==current_user.user_id,
        UserPosts.post_id==id)
    user_post = query.first()
    if not user_post:
        user_post = UserPosts(
            user_id = current_user.user_id,
            post_id = id,
            is_read = True,
        )
        db.add(user_post)
    db.commit()

    return True

@router.get("/post/read_posts/")
def get_read_posts(board_id: uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    

    posts = (db.query(UserPosts).join(Post)
        .filter(UserPosts.user_id==current_user.user_id, Post.board_id==board_id).all())

    return posts

@router.patch("/post/{id}/like/")
def like_post(id:uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    
    db.query(Post).filter(Post.post_id==id).update({'like': Post.like+1})
    db.query(UserPosts).filter(UserPosts.user_id==current_user.user_id,
        UserPosts.post_id==id).update({'favor': 'like'})

    db.commit()

    return True

@router.patch("/post/{id}/unlike/")
def hate_post(id:uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    
    db.query(Post).filter(Post.post_id==id).update({'hate': Post.like-1})
    db.query(UserPosts).filter(UserPosts.user_id==current_user.user_id,
        UserPosts.post_id==id).update({'favor': None})
    db.commit()

    return True

@router.patch("/post/{id}/hate/")
def hate_post(id:uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    
    db.query(Post).filter(Post.post_id==id).update({'hate': Post.hate+1})
    db.query(UserPosts).filter(UserPosts.user_id==current_user.user_id,
        UserPosts.post_id==id).update({'favor': 'hate'})
    db.commit()

    return True

@router.patch("/post/{id}/unhate/")
def hate_post(id:uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    
    db.query(Post).filter(Post.post_id==id).update({'hate': Post.hate-1})
    db.query(UserPosts).filter(UserPosts.user_id==current_user.user_id,
        UserPosts.post_id==id).update({'favor': None})
    db.commit()

    return True
    

@router.post("/write_post/", status_code=status.HTTP_201_CREATED)
def write_post(request: WritePost, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # request body: {“user”: “<user_name>”, “board”: “<board_name>”, “title”: “<title>”, “content”: “< content >”} 
    # return “OK” if this post is successfully recorded in your system 
    
    # query board id
    if request.board_name:
        board = db.query(Board).filter(Board.board_name==request.board_name).first()
    board_id = (request.board_id if request.board_id else board.board_id)

    # new post_id 
    post_id = uuid.uuid4()

    # Insert a new post
    new_post = Post(
        post_id = post_id,
        title = request.title,
        content = request.content,
        author_id = current_user.user_id,
        like = 0,
        hate = 0,
        post_time = datetime.now().astimezone(timezone(timedelta(hours=8))).strftime('%Y-%m-%d %H:%M:%S'),
        board_id = board_id
    )
    db.add(new_post)

    # Update user is_latest_read to true and others to false
    query = db.query(UserBoards).filter(UserBoards.board_id==board_id)
    query.update({'is_latest_read': False})
    query = db.query(UserBoards).filter(UserBoards.board_id==board_id, UserBoards.user_id==current_user.user_id)
    query.update({'is_latest_read': True})

    # Let author read the post
    user_post = UserPosts(
            user_id = current_user.user_id,
            post_id = post_id,
            is_read = True,
        )
    db.add(user_post)

    db.commit()

    return 'OK'