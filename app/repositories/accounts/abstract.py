from dataclasses import dataclass
from abc import ABC, abstractmethod

from database.schemas import AccountSchema
from repositories.accounts.schemas import AddAccountSchema, AccountID
from repositories.users.schemas import SuccessfulMessageJSON, UnsuccessfulMessageJSON, UserID


@dataclass
class AbstractAccountsRepository(ABC):
    @abstractmethod
    async def create_account(self, account: AddAccountSchema) -> AccountID:
        ...

    @abstractmethod
    async def deactivate_account(self, account_id: AccountID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        ...

    @abstractmethod
    async def activate_account(self, account_id: AccountID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        ...

    @abstractmethod
    async def get_account_by_id(self, account_id: AccountID) -> AccountSchema:
        ...

    @abstractmethod
    async def get_all_user_accounts_by_handler_id(self, handler_id: UserID) -> list[AccountSchema]:
        ...

    @abstractmethod
    async def get_total_balance_by_account_id(self, account_id: AccountID) -> float:
        ...

    @abstractmethod
    async def increase_balance(
            self,
            value: float,
            account_id: AccountID
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        ...

    @abstractmethod
    async def decrease_balance(
            self,
            value: float,
            account_id: AccountID
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        ...
