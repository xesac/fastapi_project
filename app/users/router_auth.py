from fastapi import APIRouter, Response

from app.exceptions import (
    IncorrectEmailOrPasswordException,
    IncorrectEmailOrPasswordExceptionNotEn,
    UserAlreadyExistsException,
)
from app.users.auth import authenticate_user, create_access_token, get_password_hash
from app.users.dao import UsersDAO

from .schemas import SUserAuth

router = APIRouter(
    prefix='/auth',
    tags=['Аутентификация & Авторизация']
)


@router.post('/register')
async def register_user(user_data: SUserAuth):
    existing_user = await UsersDAO.find_one_or_none(email=user_data.email)
    for i in 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя':
        if i in user_data.email.lower():
            raise IncorrectEmailOrPasswordExceptionNotEn
        elif i in user_data.password.lower():
            raise IncorrectEmailOrPasswordExceptionNotEn
    if existing_user:
        raise UserAlreadyExistsException
    hashed_password = get_password_hash(user_data.password)
    await UsersDAO.add(email=user_data.email, hashed_password=hashed_password)

@router.post('/login')
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if not user:
        raise IncorrectEmailOrPasswordException
    access_token = create_access_token({'sub': str(user.id)})
    response.set_cookie('booking_access_token', access_token, httponly=True)
    return {'access_token': access_token}

@router.post('/logout')
async def logout_user(response: Response):
    response.delete_cookie('booking_access_token')
