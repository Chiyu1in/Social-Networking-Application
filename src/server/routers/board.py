import uuid

from fastapi import APIRouter, Depends, status, HTTPException

from sqlalchemy import desc, func
from sqlalchemy.orm import Session

from database.utils import get_db
from database.models import User, Board, UserBoards, Post

from schema import BoardInfo, TokenData, PostInfo, UserBoardInfo, UserBoardOut
from oauth2 import get_current_user

router = APIRouter(
    tags=['Boards']
)

@router.get("/boards/")
def get_boards(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    boards = (db.query(UserBoards, Board.board_name).join(Board)
        .filter(UserBoards.user_id==current_user.user_id)
        .order_by(Board.board_name).all())
    boards = [
        UserBoardOut(
            id=board.UserBoards.board_id,
            board_name=board.board_name,
            is_favorite=board.UserBoards.is_favorite ,
            is_latest_read=board.UserBoards.is_latest_read,
            last_post=board.UserBoards.last_post.date()
        ) for board in boards ]

    return boards

@router.put("/update_boards/")
def update_user_boards(db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    all_boards = db.query(Board).all()
    user_boards = db.query(UserBoards).filter(UserBoards.user_id==current_user.user_id).all()
    user_boards = { user_board.board_id for user_board in user_boards}

    for board in all_boards:
        if board.board_id not in user_boards:
            last_post = db.query(Post.post_time).join(Board).filter(Board.board_id==board.board_id).order_by(desc(Post.post_time)).limit(1).first()
            new_user_board = UserBoards(
                user_id=current_user.user_id,
                board_id=board.board_id,
                is_favorite=False,
                is_latest_read=False,
                last_post=last_post.post_time
            )
            db.add(new_user_board)

    db.commit()

    return all_boards

@router.get("/board/{id}/")
def get_board(id: uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    board = db.query(Board).filter(Board.board_id==id).first()

    if not board:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Board with the id {id} is not available')

    return board

@router.patch("/board/{id}/update_favorite/")
def add_board_favorite(id: uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    query = (db.query(UserBoards)
        .filter(UserBoards.user_id==current_user.user_id, UserBoards.board_id==id))

    query.update({'is_favorite': UserBoards.is_favorite!=True})
    db.commit()


    return True 

@router.patch("/board/{id}/delete_favorite/")
def delete_board_favorite(id: uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    query = (db.query(UserBoards)
        .filter(UserBoards.user_id==current_user.user_id, UserBoards.board_id==id))

    query.update({'is_favorite': False})
    db.commit()


    return True 

@router.patch("/board/{id}/read_latest_post/")
def read_board_latest_post(id: uuid.UUID, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    query = (db.query(UserBoards)
        .filter(UserBoards.user_id==current_user.user_id, UserBoards.board_id==id))

    query.update({'is_latest_read': True})
    db.commit()


    return True 

@router.post("/is_latest_unread/")
async def is_latest_unread(request: UserBoardInfo, db: Session = Depends(get_db)):
    # request body: {“user”: “<user_name>”, “board”: “<board_name>”} 
    # return “Y” if <user_name> has not read the latest post of board <board_name>, 
    #        “N” if the latest post is read 

    board = (db.query(UserBoards).join(Board).join(User)
        .filter(User.username==request.user, 
        Board.board_name==request.board).first())
    
    return 'N' if board and board.is_latest_read else 'Y'
    
@router.post("/count_likes/")
async def count_likes(request: BoardInfo,  db: Session = Depends(get_db)):
    # request body: {“board”: “<board_name>”} 
    # return counts of total likes of all posts in the board <board_name> 

    query = (db.query(func.sum(Post.like)-func.sum(Post.hate)).join(Board)
        .filter(Board.board_name==request.board))

    return query.scalar()

@router.post("/read_latest_post/")
async def get_latest_post(request: BoardInfo,  db: Session = Depends(get_db)):
    # request body: {“board”: “<board_name>”} 
    # return .json format data of the latest post: {“author”: “< author_name>”, “board”: “<board_name>”, “post_datetime”: “<post_datetime>”, “title”: “<title>”, “article”: “< article >”} 
    
    # query last post
    post = (db.query(Post, User.username).join(Board).join(User)
        .filter(Board.board_name==request.board, User.user_id==Post.author_id) 
        .order_by(desc(Post.post_time))
        .limit(1).first())
        
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Board {request.board} or Post with it is not available')

    # response model
    show_post = PostInfo(
        post_id=post.Post.post_id,
        author=post.username,
        board=request.board,
        post_datetime=post.Post.post_time,
        title=post.Post.title,
        article=post.Post.content
    )

    return show_post




@router.post("/board/")
def create_board(request: BoardInfo, db: Session = Depends(get_db)):
    new_board = Board(
        board_id = uuid.uuid4(),
        board_name = request.board
    )
    db.add(new_board)
    db.commit()
    db.refresh(new_board)

    return new_board



# @router.delete("/board/{id}")
# async def delete_board(id: uuid.UUID, db: Session = Depends(get_db)):
#     query = query_board_id(id, db)
#     board = query.first()

#     query.delete()
#     db.commit()

#     return board