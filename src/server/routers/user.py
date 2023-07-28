import uuid

from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from database.utils import get_db
from database.models import User
from database.method import query_user_from_id, query_user_from_name

from hashing import get_password_hash
from schema import UserInfo, UserIn, UserOut, TokenData
from oauth2 import get_current_user




router = APIRouter(
    tags=['Users']
)

@router.post("/user/", response_model=UserOut)
def create_user(request: UserInfo, db: Session = Depends(get_db)):
    # request body: {'username', 'password', email', 'company', 'place', 'phone'} 

    new_user = User(
        user_id = uuid.uuid4(),
        username = request.username, 
        password = get_password_hash(request.password),
        email = request.email,
        company = request.company,
        place = request.place,
        phone = request.phone,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/user/", response_model=UserOut)
def get_user(current_user: TokenData = Depends(get_current_user)):
    
    return current_user


@router.patch("/user/")
def update_user(request: UserInfo, db: Session = Depends(get_db), current_user: TokenData = Depends(get_current_user)):
    # request body: {'email', 'company', 'place', 'phone'} 

    query = query_user_from_id(current_user.user_id, db)

    if request.email: query.update({'email': request.email})
    if request.company: query.update({'company': request.company})
    if request.place: query.update({'place': request.place})
    if request.phone: query.update({'phone': request.phone})

    db.commit()

    return True


@router.post("/has_user/")
async def has_user(request: UserIn, db: Session = Depends(get_db)):
    # request body: {“user”: “<user_name>”} 
    # return “Y” if <user_name> is a valid user, “N” if not 
    
    query = query_user_from_name(request.username, db)

    return ('Y' if query.first() else 'N')


@router.get("/user/{id}/", response_model=UserOut)
def get_user(id: uuid.UUID, db: Session = Depends(get_db)):

    user = query_user_from_id(id, db).first()

    return (user if user else False)


@router.delete("/user/{id}/")
def delete_user(id:uuid.UUID, db: Session = Depends(get_db)):

    query = query_user_from_id(id, db)

    query.delete()
    db.commit()

    return True
    


    
