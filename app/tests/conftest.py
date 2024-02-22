import pytest
from app.database.database import Base, async_session_maker, engine
from app.config.config import settings
from sqlalchemy import insert
import json
import asyncio
from app.bookings.models import Bookings
from app.hotels.rooms.models import Rooms
from app.hotels.models import Hotels
from app.users.models import Users


@pytest.fixture(scope='session', autouse=True)
async def prepare_database():
    assert settings.MODE == 'TEST'
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):
        with open(f'app/tests/mock_{model}.json', 'r') as file:
            return json.load(file)
        
    booking = open_mock_json('bookings')
    rooms = open_mock_json('rooms')
    hotels = open_mock_json('hotels')
    users = open_mock_json('users')
    print(hotels)

    async with async_session_maker() as session:
        add_bookings = insert(Bookings).values(booking)
        add_rooms = insert(Rooms).values(rooms)
        add_hotels = insert(Hotels).values(hotels)
        add_users = insert(Users).values(users)

        lst = [add_bookings, add_hotels, add_rooms, add_users]
        await [session.execute(req) for req in lst]
        await session.commit()

@pytest.fixture(scope='session')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()