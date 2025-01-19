from datetime import date

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    ...


class Users(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    balance_id: Mapped[str] = mapped_column(nullable=True)
    first_name: Mapped[str]
    second_name: Mapped[str]
    surname: Mapped[str] = mapped_column(nullable=True)
    date_of_birth: Mapped[date]
    registration_date: Mapped[date]
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
