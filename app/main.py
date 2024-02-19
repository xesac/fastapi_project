from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.admin.views import BookingsAdmin, HotelsAdmin, UsersAdmin, RoomsAdmin
from app.bookings.router import router as router_bookings
from app.users.router_auth import router as router_auth
from app.users.router_users import router as router_users
from app.hotels.router import router as router_hotels
from app.hotels.rooms.router import router as router_rooms
from app.pages.router import router as router_pages
from app.images.router import router as router_images
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from contextlib import asynccontextmanager
from redis import asyncio as aioredis
from app.config.config import settings
from app.database.database import engine
from sqladmin import Admin

@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}')
    FastAPICache.init(RedisBackend(redis), prefix='cache')

    print('Запущено')
    yield
    print('Завершено')
    



# создание приложения
app = FastAPI(lifespan=lifespan)

admin = Admin(app, engine=engine)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)


app.mount('/static', StaticFiles(directory='app/static'), 'static')

# добавление роутера
app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_rooms)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
