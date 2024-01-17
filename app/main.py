from fastapi import FastAPI

from app.bookings.router import router as router_bookings

# создание приложения
app = FastAPI()


# добавление роутера
app.include_router(router_bookings)

# генератор сессий
# async def get_async_session():
#     async with async_session_maker() as async_session:
#         yield async_session