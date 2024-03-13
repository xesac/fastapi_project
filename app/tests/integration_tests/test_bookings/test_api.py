import pytest
from httpx import AsyncClient
from datetime import date

@pytest.mark.parametrize("room_id, date_from, date_to, booked_rooms, status_code", [
    (4, "2030-05-01", "2030-05-15", 5, 200),
    (4, "2030-05-01", "2030-05-15", 10, 200),
    (1, "2030-05-05", "2030-05-01", 2, 400),
    (1, "2030-05-05", "2030-08-01", 2, 400)
    ])
async def test_add_and_get_booking(authenticated_ac: AsyncClient, room_id: int, date_from: date, date_to: date, booked_rooms: int, status_code: int):
    response = await authenticated_ac.post('/bookings', params={
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to
    })

    assert response.status_code == status_code


async def test_get_bookings(authenticated_ac: AsyncClient):
    response = await authenticated_ac.get('/bookings')
    assert response.status_code == 200


