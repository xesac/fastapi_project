from fastapi import FastAPI

from app.bookings.router import router as router_bookings
from app.users.router_auth import router as router_auth
from app.users.router_users import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
# создание приложения
app = FastAPI()


# добавление роутера
app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_rooms)
app.include_router(router_hotels)

