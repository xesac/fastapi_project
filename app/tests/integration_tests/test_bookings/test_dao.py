from datetime import date

import pytest

from app.bookings.dao import BookingDAO


@pytest.mark.parametrize('user_id, room_id, date_from, date_to', [
    (1, 5, date(2021, 1, 5), date(2021, 1, 15)),
    (1, 5, date(2021, 1, 5), date(2021, 1, 8))
])
async def test_add_and_get_booking(user_id: int, room_id: int, date_from: date, date_to: date):
    response = await BookingDAO.add(user_id, room_id, date_from, date_to)

    assert response.total_days > 1
    assert response.user_id == 1
    assert response.room_id == 5

    new_booking = await BookingDAO.find_by_id(response.id)
    assert new_booking is not None

