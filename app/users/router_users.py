from fastapi import APIRouter, Depends

from .dependencies import get_current_admin_user, get_current_user
from .models import Users

router = APIRouter(
    prefix='/users',
    tags=['Пользователи']
)



@router.get('/me')
async def read_users_me(current_user: Users = Depends(get_current_user)):
    return current_user

@router.get('/all')
async def read_all_userS(current_user: Users = Depends(get_current_admin_user)):
    return current_user