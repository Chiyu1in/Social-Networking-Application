from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.orm import Session

from database.utils import get_db
from database.models import User

from hashing import verify_password

from schema import Token
from oauth2 import create_access_token


router = APIRouter(
    tags=['Authentication']
)

@router.post("/login", response_model=Token)
def login_for_access_token(request: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username==request.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'User not found!!')
    if not verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
            detail=f'Incorrect username or password')

    # 傳回的data info
    user_out = {
        'user_id': user.user_id.hex,
        'username': user.username,
        'email': user.email,
        'company': user.company,
        'place': user.place,
        'phone': user.phone
    }
    access_token = create_access_token(data=user_out)

    return {"access_token": access_token, "token_type": "bearer"}

