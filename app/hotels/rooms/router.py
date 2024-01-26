from fastapi import APIRouter
from .dao import RoomsDAO
from datetime import date


router = APIRouter(
    prefix='/hotels',
    tags=['Комнаты']
)

@router.get('/rooms/{hotel_id}')
async def get_rooms_by_hotel_id(hotel_id: int):
    return await RoomsDAO.find_all(hotel_id=hotel_id)


@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    return await RoomsDAO.find_all_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)