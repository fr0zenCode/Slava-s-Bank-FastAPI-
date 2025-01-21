from dataclasses import dataclass
from abc import ABC, abstractmethod

from repositories.accounts.schemas import AddAccountSchema, AccountID


@dataclass
class AbstractAccountsRepository(ABC):
    @abstractmethod
    async def create_account(self, account: AddAccountSchema) -> AccountID:
        ...

    @abstractmethod
    async def deactivate_account(self):
        ...

    @abstractmethod
    async def activate_account(self):
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
    