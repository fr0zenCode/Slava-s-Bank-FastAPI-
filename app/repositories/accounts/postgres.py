from dataclasses import dataclass

from .abstract import AbstractAccountsRepository


@dataclass
class SQLAlchemyPostgresAccountRepository(AbstractAccountsRepository):

    async def create_account(self):
        ...

    async def deactivate_account(self):
        ...

    async def get_account_by_id(self):
        ...

    async def get_all_user_accounts_by_handler_id(self):
        ...

    async def increase_balance(self):
        ...

    async def decrease_balance(self):
        ...
