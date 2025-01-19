import re
from typing import ClassVar
from datetime import date

from pydantic import BaseModel, EmailStr, field_validator

from app.services.users.exceptions import InvalidPhoneNumberException


class AddUserSchema(BaseModel):

    first_name: str
    last_name: str
    surname: str

    date_of_birth: date

    email: EmailStr
    phone: str

    RUSSIAN_PHONE_NUMBER_REGEX: ClassVar[re.Pattern] = re.compile(r"^(\+7|8)\d{10}$")

    @field_validator("phone")
    def validate_russian_phone_number(cls, value):
        if not cls.RUSSIAN_PHONE_NUMBER_REGEX.match(value):
            raise InvalidPhoneNumberException(phone_number=value)
        return value
