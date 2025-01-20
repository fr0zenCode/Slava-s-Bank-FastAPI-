from dataclasses import dataclass
from abc import ABC, abstractmethod

from repositories.users.schemas import AddUserSchema, UserID


@dataclass
class AbstractUsersRepository(ABC):
    @abstractmethod
    async def create_user(self, user: AddUserSchema) -> UserID:
        ...

    @abstractmethod
    async def deactivate_user(self):
        ...

    @abstractmethod
    async def get_user_by_id(self):
        ...

    @abstractmethod
    async def get_user_by_email(self):
        ...

    @abstractmethod
    async def get_user_by_phone(self):
        ...
