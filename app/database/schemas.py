from datetime import date, datetime

from pydantic import BaseModel, EmailStr

from database.enums import AccountStatus, TransactionStatus, OperationType


class UserSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    surname: str | None
    date_of_birth: date
    registration_date: date
    phone: str
    email: EmailStr
    is_active: bool


class AccountSchema(BaseModel):
    id: str
    handler_id: str
    creation_date: date
    inspiration_date: date
    balance: float
    account_status: AccountStatus


class TransactionSchema(BaseModel):
    id: str
    amount: float
    initializer_id: str
    recipient_id: str
    status: TransactionStatus
    transaction_date: datetime
