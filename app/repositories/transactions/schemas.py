from datetime import datetime

from pydantic import BaseModel

from database.enums import TransactionStatus, OperationType


class AddTransactionFromEndpointsSchema(BaseModel):
    amount: float
    initializer_id: str
    recipient_id: str


class AddTransactionSchema(AddTransactionFromEndpointsSchema):
    id: str
    status: TransactionStatus
    operation_type: OperationType
    transaction_date: datetime


class TransactionSchema(AddTransactionSchema):
    ...


class TransactionID(BaseModel):
    value: str
