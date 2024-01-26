from app.dao.dao import BaseDAO
from .models import Hotels
from app.database.database import async_session_maker
from sqlalchemy import select, and_, func



class HotelsDAO(BaseDAO):
    model = Hotels

    @classmethod
    async def find_by_location(cls, location: str):
        async with async_session_maker() as session:
            query = select(Hotels).where(
                and_(
                    Hotels.location.contains(location),
                    Hotels.rooms_quantity > 0
                ))
                    
            result = await session.execute(query)
            return result.mappings().all()
