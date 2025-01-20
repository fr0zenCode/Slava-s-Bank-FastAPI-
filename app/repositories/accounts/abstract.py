from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AbstractAccountsRepository(ABC):
    @abstractmethod
    async def create_account(self):
        ...

    @abstractmethod
    async def deactivate_account(self):
        ...

    @abstractmethod
    async def get_account_by_id(self):
        ...

    @abstractmethod
    async def get_all_user_accounts_by_handler_id(self):
        ...

    @abstractmethod
    async def increase_balance(self):
        ...

    @abstractmethod
    async def decrease_balance(self):
        ...
    