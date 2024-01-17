from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from app.config.config import settings




#создание движка
engine = create_async_engine(settings.DATABASE_URL)

# создаем бд
class Base(DeclarativeBase):
    pass


async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)
