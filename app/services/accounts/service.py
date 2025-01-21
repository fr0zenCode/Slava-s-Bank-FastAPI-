from datetime import timedelta, date
from uuid import uuid4
from dataclasses import dataclass

from repositories.accounts.postgres import get_sqlalchemy_postgres_accounts_repository
from repositories.accounts.schemas import AddAccountSchema, AccountID, AddAccountFromEndpointsSchema


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


def get_accounts_service() -> AccountsService:
    return AccountsService()
