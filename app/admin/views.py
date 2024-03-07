from sqladmin import ModelView

from app.bookings.models import Bookings
from app.hotels.models import Hotels
from app.hotels.rooms.models import Rooms
from app.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email]
    column_details_exclude_list = [Users.hashed_password]
    name = 'Пользователь'
    name_plural = 'Пользователи'
    can_delete = False
    can_edit = False
    page_size = 20
    icon = 'fa-solid fa-user'

class HotelsAdmin(ModelView, model=Hotels):
    column_list = '__all__'
    name = 'Отель'
    name_plural = 'Отели'
    icon = 'fa-solid fa-hotel'

class BookingsAdmin(ModelView, model=Bookings):
    column_list = '__all__'
    name = 'Бронь'
    name_plural = 'Брони'
    icon = 'fa-solid fa-book'


class RoomsAdmin(ModelView, model=Rooms):
    column_list = '__all__'
    name = 'Комната'
    name_plural = 'Комнаты'
    icon = 'fa-solid fa-bed'