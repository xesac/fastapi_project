from fastapi import Request, Depends
from jose import jwt, JWTError, ExpiredSignatureError
from app.config.config import settings
from .dao import UsersDAO
from .models import Users
from app.exceptions import TokenExpiredException, TokenAbsentException, IncorrectTokenException, UserIsNotPresentException

def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, settings.ALGHORITM
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDAO.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user


async def get_current_admin_user(current_user: Users = Depends(get_current_user)):
    # if current_user.role != 'admin':
    #     raise HTTPException(401)
    return await UsersDAO.find_all()