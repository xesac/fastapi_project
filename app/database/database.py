from sqlalchemy import NullPool
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

from app.config.config import settings

if settings.MODE == 'TEST':
    DATABASE_URL = settings.TEST_DATABASE_URL
    DATABASE_PARAMS = {'poolclass': NullPool}
else:
    DATABASE_URL = settings.DATABASE_URL
    DATABASE_PARAMS = {}

print(DATABASE_URL)
#создание движка
engine = create_async_engine(DATABASE_URL, **DATABASE_PARAMS)

# создаем бд
class Base(DeclarativeBase):
    pass


async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
