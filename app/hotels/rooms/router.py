from datetime import date

from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.bookings.models import Bookings
from app.database.database import async_session_maker

from ..models import Hotels
from .dao import RoomsDAO
from .models import Rooms

router = APIRouter(
    prefix='/hotels',
    tags=['Комнаты']
)

@router.get('/rooms/{hotel_id}')
async def get_rooms_by_hotel_id(hotel_id: int):
    return await RoomsDAO.find_all(hotel_id=hotel_id)

@router.get('/rooms')
async def get_rooms():
    return await RoomsDAO.find_all()

@router.get("/{hotel_id}/rooms")
async def get_rooms(hotel_id: int, date_from: date, date_to: date):
    return await RoomsDAO.find_all_rooms(hotel_id=hotel_id, date_from=date_from, date_to=date_to)

@router.get('/example/no_orm')
async def get_noorm():
    async with async_session_maker() as session:
        query = (
            select(Rooms.__table__.columns, Hotels.__table__.columns, Bookings.__table__.columns)
            .join(Hotels, Rooms.hotel_id == Hotels.id)
            .join(Bookings, Bookings.room_id == Rooms.id)
        )
        res = await session.execute(query)
        return res.mappings().all()


@router.get('/example/orm')
async def get_orm():
    async with async_session_maker() as session:
        query = (
            select(Rooms)
            .options(selectinload(Rooms.hotel))
            .options(selectinload(Rooms.booking))
        )
        res = await session.execute(query)
        res = res.scalars().all()
        res = jsonable_encoder(res)
        return res