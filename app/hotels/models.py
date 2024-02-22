from app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, JSON
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.hotels.rooms.models import Rooms

class Hotels(Base):
    __tablename__ = 'hotels'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str]
    location: Mapped[str]
    services: Mapped[list[str]] = mapped_column(JSON, nullable=True)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]

    room: Mapped[list['Rooms']] = relationship(back_populates='hotel')



    def __str__(self):
        return f'{self.name}'