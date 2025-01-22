from datetime import timedelta, date
from uuid import uuid4
from dataclasses import dataclass

from database.schemas import AccountSchema
from repositories.accounts.postgres import get_sqlalchemy_postgres_accounts_repository
from repositories.accounts.schemas import AddAccountSchema, AccountID, AddAccountFromEndpointsSchema
from repositories.users.schemas import SuccessfulMessageJSON, UnsuccessfulMessageJSON, UserID


@dataclass
class AccountsService:

    accounts_repository = get_sqlalchemy_postgres_accounts_repository()

    @staticmethod
    def _generate_account_id() -> str:
        return f"account-{str(uuid4())}"

    async def create_account(self, account: AddAccountFromEndpointsSchema) -> AccountID:
        add_account_schema = AddAccountSchema(
            id=self._generate_account_id(),
            handler_id=account.handler_id,
            creation_date=date.today(),
            inspiration_date=date.today() + timedelta(days=(5 * 365)),
            balance=account.balance,
            account_status=account.account_status
        )
        new_account_id = await self.accounts_repository.create_account(account=add_account_schema)
        return new_account_id

    async def deactivate_account(self, account_id: AccountID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        await self.accounts_repository.deactivate_account(account_id=account_id)
        return SuccessfulMessageJSON()

    async def activate_account(self, account_id: AccountID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        await self.accounts_repository.activate_account(account_id=account_id)
        return SuccessfulMessageJSON()

    async def get_account_by_id(self, account_id: AccountID) -> AccountSchema:
        account = await self.accounts_repository.get_account_by_id(account_id=account_id)
        return account

    async def get_user_accounts_by_handler_id(self, handler_id: UserID) -> list[AccountSchema]:
        accounts = await self.accounts_repository.get_all_user_accounts_by_handler_id(handler_id=handler_id)
        return accounts

    async def get_total_balance_by_account_id(self, account_id: AccountID) -> float:
        balance = await self.accounts_repository.get_total_balance_by_account_id(account_id=account_id)
        return balance

    async def increase_balance(
            self,
            value: float,
            account_id: AccountID
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        await self.accounts_repository.increase_balance(value=value, account_id=account_id)
        return SuccessfulMessageJSON()

    async def decrease_balance(
            self,
            value: float,
            account_id: AccountID
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        await self.accounts_repository.decrease_balance(value=value, account_id=account_id)
        return SuccessfulMessageJSON()


def get_accounts_service() -> AccountsService:
    return AccountsService()
