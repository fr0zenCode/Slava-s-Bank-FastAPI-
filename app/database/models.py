from datetime import date, timedelta, datetime
from typing import Optional

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.core import Base
from database.enums import TransactionStatus, AccountStatus
from database.schemas import UserSchema, AccountSchema, TransactionSchema


class Users(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(primary_key=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    surname: Mapped[Optional[str]]
    date_of_birth: Mapped[date]
    registration_date: Mapped[date] = mapped_column(default=date.today())
    phone: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    handled_accounts: Mapped[list["Accounts"]] = relationship("Accounts", back_populates="handler")

    def convert_to_pydantic_model(self) -> UserSchema:
        return UserSchema(
            id=self.id,
            first_name=self.first_name,
            last_name=self.last_name,
            surname=self.surname,
            date_of_birth=self.date_of_birth,
            registration_date=self.registration_date,
            phone=self.phone,
            email=self.email,
            is_active=self.is_active
        )


class Accounts(Base):
    __tablename__ = "accounts"

    id: Mapped[str] = mapped_column(primary_key=True)
    handler_id: Mapped[str] = mapped_column(ForeignKey("users.id"))
    creation_date: Mapped[date] = mapped_column(default=date.today())
    inspiration_date: Mapped[date] = mapped_column(default=date.today() + timedelta(days=(5 * 365)))
    balance: Mapped[float] = mapped_column(default=0.00)
    account_status: Mapped[AccountStatus] = mapped_column(default=AccountStatus.ACTIVE)

    handler: Mapped["Users"] = relationship("Users", back_populates="handled_accounts")

    def convert_to_pydantic_model(self) -> AccountSchema:
        return AccountSchema(
            id=self.id,
            handler_id=self.handler_id,
            creation_date=self.creation_date,
            inspiration_date=self.inspiration_date,
            balance=self.balance,
            account_status=self.account_status
        )


class Transactions(Base):
    __tablename__ = "transactions"

    id: Mapped[str] = mapped_column(primary_key=True)
    amount: Mapped[float] = mapped_column(nullable=False)
    initializer_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    recipient_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), nullable=False)
    status: Mapped[TransactionStatus] = mapped_column(default=TransactionStatus.PENDING)
    transaction_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)

    initializer: Mapped["Accounts"] = relationship("Accounts", foreign_keys=[initializer_id])
    recipient: Mapped["Accounts"] = relationship("Accounts", foreign_keys=[recipient_id])

    def convert_to_pydantic_model(self) -> TransactionSchema:
        return TransactionSchema(
            id=self.id,
            amount=self.amount,
            initializer_id=self.initializer_id,
            recipient_id=self.recipient_id,
            status=self.status,
            transaction_date=self.transaction_date
        )


class Passwords(Base):
    __tablename__ = "passwords"

    user_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), primary_key=True)
    password: Mapped[str]


class Sessions(Base):
    __tablename__ = "sessions"

    user_id: Mapped[str] = mapped_column(ForeignKey("accounts.id"), primary_key=True)
    session_id: Mapped[str] = mapped_column(unique=True)
    banned: Mapped[bool] = mapped_column(default=False)
