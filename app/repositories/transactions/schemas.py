from datetime import datetime

from pydantic import BaseModel

from database.enums import TransactionStatus


class AddTransactionFromEndpointsSchema(BaseModel):
    amount: float
    initializer_id: str
    recipient_id: str


class AddTransactionSchema(AddTransactionFromEndpointsSchema):
    id: str
    status: TransactionStatus
    transaction_date: datetime


class TransactionSchema(AddTransactionSchema):
    ...


class TransactionID(BaseModel):
    value: str
