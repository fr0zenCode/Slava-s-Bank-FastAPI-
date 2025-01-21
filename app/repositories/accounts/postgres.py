from dataclasses import dataclass

from sqlalchemy import insert

from database.models import Accounts
from database.core import get_sqlalchemy_async_database_helper
from .abstract import AbstractAccountsRepository
from .schemas import AddAccountSchema, AccountID


@dataclass
class SQLAlchemyPostgresAccountRepository(AbstractAccountsRepository):

    database_helper = get_sqlalchemy_async_database_helper()
    session_factory = database_helper.get_session_factory()

    async def create_account(self, account: AddAccountSchema) -> AccountID:
        async with self.session_factory() as session:
            stmt = insert(Accounts).values(
                id=account.id,
                handler_id=account.handler_id,
                creation_date=account.creation_date,
                inspiration_date=account.inspiration_date,
                balance=account.balance,
                account_status=account.account_status
            ).returning(Accounts.id)
            response = await session.execute(stmt)
            await session.commit()
            return AccountID(value=response.scalar_one())

    async def deactivate_account(self):
        ...

    async def activate_account(self):
        ...

    async def get_account_by_id(self):
        ...

    async def get_all_user_accounts_by_handler_id(self):
        ...

    async def increase_balance(self):
        ...

    async def decrease_balance(self):
        ...


def get_sqlalchemy_postgres_accounts_repository() -> SQLAlchemyPostgresAccountRepository:
    return SQLAlchemyPostgresAccountRepository()
