from fastapi import APIRouter, Depends
from pydantic import TypeAdapter
from app.task.tasks import send_booking_confirmation_email
from .dao import BookingDAO
from app.users.models import Users
from .schemas import SBooking
from app.users.dependencies import get_current_user
from datetime import date
from fastapi import BackgroundTasks


router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)


@router.get('')
async def get_bookings(user: Users = Depends(get_current_user)) -> list[SBooking]:
    return await BookingDAO.find_all(user_id=user.id)

@router.post("")
async def add_booking(
        #background_task: BackgroundTasks,
        room_id: int,
        date_from: date,
        date_to: date,
        user: Users = Depends(get_current_user)
):
    booking = await BookingDAO.add(
        user_id=user.id,
        room_id=room_id,
        date_from=date_from,
        date_to=date_to
    )

    booking_dict = TypeAdapter(SBooking).validate_python(booking).model_dump()

    #вариант с celery
    send_booking_confirmation_email.delay(booking_dict, user.email)

    #вариант с background Task
    #background_task.add_task(send_booking_confirmation_email, booking_dict, user.email)
    return booking_dict

    
# @router.delete('/{booking_id}')
# async def delete_booking(booking_id: int, user: Users = Depends(get_current_user), booking: Bookings = Depends(get_bookings)):
#     return await BookingDAO.delete_booking(booking_id)

