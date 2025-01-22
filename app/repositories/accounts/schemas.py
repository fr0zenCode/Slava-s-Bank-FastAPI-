from datetime import date

from pydantic import BaseModel

from database.enums import AccountStatus


class AddAccountFromEndpointsSchema(BaseModel):
    handler_id: str
    balance: float
    account_status: AccountStatus


class AddAccountSchema(AddAccountFromEndpointsSchema):
    id: str
    inspiration_date: date
    creation_date: date


class AccountID(BaseModel):
    value: str


class Balance(BaseModel):
    value: float
