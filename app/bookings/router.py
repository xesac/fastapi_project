from fastapi import APIRouter, Path, Query
from .dao import BookingDAO
from typing import Annotated
from fastapi.responses import JSONResponse
from .schemas import SBooking

router = APIRouter(
    prefix='/bookings',
    tags=['Бронирование']
)





@router.get('')
async def get_bookings() -> list[SBooking]:
    return await BookingDAO.find_all()