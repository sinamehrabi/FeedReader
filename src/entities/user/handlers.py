from fastapi import APIRouter, status, Depends
from sqlalchemy.orm import Session
from src.database import get_db
from .schemas import UserSignDTO, UserTokenDTO, UserInfoDTO
from .services import UserService
from ...utils import verify_token

router = APIRouter()


@router.post("/users/register", status_code=status.HTTP_201_CREATED, response_model=UserTokenDTO)
def user_registration(user_data: UserSignDTO, db: Session = Depends(get_db)):
    return UserService(db).register_user(user_data)


@router.post("/users/login", status_code=status.HTTP_200_OK, response_model=UserTokenDTO)
def user_login(user_data: UserSignDTO, db: Session = Depends(get_db)):
    return UserService(db).login_user(user_data)


@router.get("/users/me", status_code=status.HTTP_200_OK, response_model=UserInfoDTO)
def user_info(db: Session = Depends(get_db), user_id: int = Depends(verify_token)):
    return UserService(db).get_user_info(user_id)
