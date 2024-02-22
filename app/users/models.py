from app.database.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.bookings.models import Bookings


class Users(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]
    hashed_password: Mapped[str]

    booking: Mapped[list['Bookings']] = relationship(back_populates='user')



    def __str__(self):
        return f'{self.email}'
        