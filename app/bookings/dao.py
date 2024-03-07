from datetime import date

from fastapi import Depends
from fastapi.responses import JSONResponse
from sqlalchemy import and_, delete, func, insert, select, update


from app.bookings.models import Bookings
from app.dao.dao import BaseDAO
from app.database.database import async_session_maker
from app.exceptions import RoomCannotBeBooked
from app.hotels.rooms.models import Rooms
from app.users.dependencies import get_current_user
from app.users.models import Users

from .models import Bookings


class BookingDAO(BaseDAO):
    model = Bookings

    @classmethod
    async def delete_booking(
        cls, booking_id: int, user: Users = Depends(get_current_user)
    ):
        if user:
            async with async_session_maker() as session:
                booking = select(Bookings).where(
                    and_(Bookings.id == booking_id, Bookings.user_id == user.id)
                )
                booking = await session.execute(booking)
                result = booking.mappings().all()
                if result:
                    delet = delete(Bookings).where(
                        and_(Bookings.user_id == user.id, Bookings.id == booking_id)
                    )
                    res = await session.execute(delet)
                    res = await session.commit()
                    return JSONResponse(content={"message": "Номер удален"})
                else:
                    return JSONResponse(content={"message": "Такого номера нет"})
        else:
            return JSONResponse(content={"message": "Ошибка"})

    @classmethod
    async def add(cls, user_id: int, room_id: int, date_from: date, date_to: date):
        """WITH booked_rooms AS (
            SELECT * FROM bookings
            WHERE room_id = 1 AND
            date_from <= '2033-06-20' AND date_to >= '2033-05-15'
        )

        SELECT rooms.quantity - COUNT(booked_rooms.room_id) FROM rooms
        LEFT JOIN booked_rooms ON booked_rooms.room_id = rooms.id
        WHERE rooms.id = 1
        GROUP BY rooms.quantity, booked_rooms .room_id"""
        async with async_session_maker() as session:
            booked_rooms = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == 1,
                        and_(
                            Bookings.date_from <= date_to, Bookings.date_to >= date_from
                        ),
                    )
                )
                .cte("booked_rooms")
            )

            get_rooms_left = (
                select(Rooms.quantity - func.count(booked_rooms.c.room_id))
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            rooms_left = await session.execute(get_rooms_left)

            rooms_left = rooms_left.scalar()

            if rooms_left > 0:
                get_price = select(Rooms.price).filter_by(id=room_id)
                price = await session.execute(get_price)
                price: int = price.scalar()
                add_booking = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(Bookings)
                )

                stmt = (
                    update(Rooms)
                    .where(Rooms.id == room_id)
                    .values(quantity=Rooms.quantity - 1)
                )
                new_booking = await session.execute(add_booking)
                rooms = await session.execute(stmt)
                await session.commit()
                return new_booking.scalar()
            else:
                raise RoomCannotBeBooked
