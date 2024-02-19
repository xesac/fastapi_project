from app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, JSON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.bookings.models import Bookings
    from app.hotels.models import Hotels

class Rooms(Base):
    __tablename__ = 'rooms'

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey('hotels.id'))
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[int]
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    quantity: Mapped[int]
    image_id: Mapped[int]

    hotel: Mapped['Hotels'] = relationship(back_populates='room')
    booking: Mapped['Bookings'] = relationship(back_populates='room')



    def __str__(self):
        return f'{self.name}'