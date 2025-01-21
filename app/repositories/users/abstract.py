from dataclasses import dataclass
from abc import ABC, abstractmethod

from pydantic import EmailStr

from repositories.users.schemas import (
    AddUserSchema,
    UserID,
    SuccessfulMessageJSON,
    UnsuccessfulMessageJSON,
    UserSchema, PhoneNumber
)


@dataclass
class AbstractUsersRepository(ABC):
    @abstractmethod
    async def create_user(self, user: AddUserSchema) -> UserID:
        ...

    @abstractmethod
    async def deactivate_user_by_id(self, user_id: UserID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        ...

    @abstractmethod
    async def activate_user_by_id(self, user_id: UserID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        ...

    @abstractmethod
    async def get_user_by_id(self, user_id: UserID) -> UserSchema:
        ...

    @abstractmethod
    async def get_user_by_email(self, email: EmailStr) -> UserSchema:
        ...

    @abstractmethod
    async def get_user_by_phone(self, phone: PhoneNumber) -> UserSchema:
        ...
