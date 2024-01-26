from app.dao.dao import BaseDAO
from .models import Rooms
from app.database.database import async_session_maker
from sqlalchemy import select, func, and_
from app.bookings.models import Bookings

class RoomsDAO(BaseDAO):
    model = Rooms
    
    @classmethod
    async def find_all_rooms(cls, hotel_id: int, date_from, date_to):
        async with async_session_maker() as session:
            booked_rooms = select(Bookings).where(
                and_(
                    Bookings.room_id == 1,
                    and_(
                        Bookings.date_from <= date_to,
                        Bookings.date_to >= date_from
                    )
                )
            ).cte('booked_rooms')
            get_rooms_left = select(Rooms.quantity - func.count(booked_rooms.c.room_id)).select_from(Rooms).join(
                booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True
            ).where(Rooms.id == hotel_id).group_by(
                Rooms.quantity, booked_rooms.c.room_id
            )

            
            rooms_left = await session.execute(get_rooms_left)

            rooms_left = rooms_left.scalar()
            print(rooms_left)
            query = select(Rooms.__table__.columns).where(Rooms.hotel_id == hotel_id)
            res = await session.execute(query)
            return res.mappings().all()
