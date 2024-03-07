import pytest
from httpx import AsyncClient

from app.users.dao import UsersDAO


@pytest.mark.parametrize('id, email, exist', [
    (1, 'test@test.com', True),
    (2, 'artem@example.com', True),
    (3, 'test2@test2.com', False)
])
async def test_find_user_by_id(id: int, email: str, exist: bool):
    user = await UsersDAO.find_by_id(id)
    
    if exist:
        assert user
        assert user.id == id
        assert user.email == email
    else:
        assert not user


async def test_find_all_users():
    users = await UsersDAO.find_all()
    assert len(users) > 0