import pytest
from httpx import AsyncClient
from datetime import date

@pytest.mark.parametrize("room_id,date_from,date_to,booked_rooms,status_code", *[
    [(4, "2030-05-01", "2030-05-15", i, 200) for i in range(3, 11)] +
    [(4, "2030-05-01", "2030-05-15", 10, 409)] * 2
    ])
async def test_add_and_get_booking(authenticated_ac: AsyncClient, room_id: int, date_from: date, date_to: date, booked_rooms: int, status_code: int):
    response = await authenticated_ac.post('/bookings', params={
        'room_id': room_id,
        'date_from': date_from,
        'date_to': date_to
    })

    assert response.status_code == status_code

    response = await authenticated_ac.get('/bookings')
    
    assert len(response.json()) == booked_rooms

    