from contextlib import asynccontextmanager
import time
from app.prometheus.router import router as router_prometheus
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from sqladmin import Admin
from prometheus_fastapi_instrumentator import Instrumentator
from app.admin.auth import authentication_backend
from app.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from app.bookings.router import router as router_bookings
from app.config.config import settings
from app.database.database import engine
from app.hotels.rooms.router import router as router_rooms
from app.hotels.router import router as router_hotels
from app.images.router import router as router_images
from app.pages.router import router as router_pages
from app.users.router_auth import router as router_auth
from app.users.router_users import router as router_users
import sentry_sdk
from app.logger import logger
from fastapi_versioning import VersionedFastAPI, version
from app.importer.router import router as router_importer





@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = aioredis.from_url(f'redis://{settings.REDIS_HOST}:{settings.REDIS_PORT}')
    FastAPICache.init(RedisBackend(redis), prefix='cache')
    print('Запущено')
    yield
    print('Завершено')



# создание приложения
app = FastAPI(lifespan=lifespan, title='Островок', description='Бронирование отелей')




# добавление роутера
app.include_router(router_users)
app.include_router(router_auth)
app.include_router(router_bookings)
app.include_router(router_rooms)
app.include_router(router_hotels)
app.include_router(router_pages)
app.include_router(router_images)
app.include_router(router_importer)
app.include_router(router_prometheus)


instrumentator = Instrumentator(
    should_group_status_codes=False,
    excluded_handlers=['.*admin', '/metrics']
)
instrumentator.instrument(app).expose(app)

app = VersionedFastAPI(app, 
    version_format='{major}',
    prefix_format='/v{major}'
)




app.mount('/static', StaticFiles(directory='app/static'), 'static')
admin = Admin(app, engine=engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(BookingsAdmin)
admin.add_view(RoomsAdmin)






# sentry_sdk.init(
#     dsn='https://141592df8d6868f69bf447a5d622438c@o4506869734309888.ingest.us.sentry.io/4506869736538112',
#     traces_sample_rate=1.0
# )






# @app.middleware('http')
# async def add_proccess_time_handler(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     proccess_time = time.time() - start_time
#     response.headers['X-Proccess-Time'] = str(proccess_time)
#     logger.info('Request execution time', extra={
#         'proccess_time': round(proccess_time, 4)
#     })
#     return response