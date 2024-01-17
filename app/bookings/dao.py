from app.database.database import async_session_maker
from sqlalchemy import select
from app.bookings.models import Bookings
from app.dao.dao import BaseDAO
from .models import Bookings

class BookingDAO(BaseDAO):
    model = Bookings