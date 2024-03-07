import pytest
from httpx import AsyncClient


@pytest.mark.parametrize('email, password, status_code', [
    ('kotopes@mail.ru', 'kotopes', 200),
    ('AFAGEGAE@mail.ru', 'GEGEGE', 200),
    ('kotopes@mail.ru', 'k0topes', 409),
    ('abcde', 'afeea', 422),
    ('', 'e6ag465', 422),
    ('aegeagaeg', '', 422),
    ('aegaeg@mail.ru', 'egag6ф4654', 401)
])
async def test_register_user(email: str, password: str, status_code: int, ac: AsyncClient):
    response = await ac.post('/auth/register', json={
        "email": email,
        "password": password
    })
    assert response.status_code == status_code


@pytest.mark.parametrize('email, password, status_code', [
    ('test@test.com', 'test', 200),
    ('artem@example.com', 'artem', 200),
    ('wrong@mail.ru', 'eageag', 401)
])
async def test_login_user(email: str, password: str, status_code: int, ac: AsyncClient):
    response = await ac.post('/auth/login', json={
        'email': email,
        'password': password
    })
    assert response.status_code == status_code