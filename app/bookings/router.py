from fastapi import APIRouter, Depends
from .dao import BookingDAO
from app.users.models import Users
from .schemas import SBooking
from app.users.dependencies import get_current_user
from datetime import date
from app.exceptions import RoomCannotBeBooked
from.models import Bookings

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post('/')
async def add_booking(room_id: int, date_from: date, date_to: date, user: Users = Depends(get_current_user)):
    booking = await BookingDAO.add(user.id, room_id, date_from, date_to)
    if not booking:
        raise RoomCannotBeBooked
    
@router.delete('/{booking_id}')
async def delete_booking(booking_id: int, user: Users = Depends(get_current_user), booking: Bookings = Depends(get_bookings)):
    print(booking)

