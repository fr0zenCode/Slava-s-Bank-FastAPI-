from dataclasses import dataclass

from sqlalchemy import insert, update, select

from database.enums import AccountStatus
from database.models import Accounts
from database.core import get_sqlalchemy_async_database_helper
from database.schemas import AccountSchema
from .abstract import AbstractAccountsRepository
from .schemas import AddAccountSchema, AccountID
from ..users.schemas import SuccessfulMessageJSON, UnsuccessfulMessageJSON, UserID


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

    async def deactivate_account(self, account_id: AccountID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        async with self.session_factory() as session:
            stmt = update(Accounts)\
                .where(Accounts.id == account_id.value)\
                .values(account_status=AccountStatus.DISABLED)
            await session.execute(stmt)
            await session.commit()
            return SuccessfulMessageJSON()

    async def activate_account(self, account_id: AccountID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        async with self.session_factory() as session:
            stmt = update(Accounts).where(Accounts.id == account_id.value).values(account_status=AccountStatus.ACTIVE)
            await session.execute(stmt)
            await session.commit()
            return SuccessfulMessageJSON()

    async def get_account_by_id(self, account_id: AccountID) -> AccountSchema:
        async with self.session_factory() as session:
            stmt = select(Accounts).where(Accounts.id == account_id.value)
            account = await session.execute(stmt)
            return account.scalar_one().convert_to_pydantic_model()

    async def get_all_user_accounts_by_handler_id(self, handler_id: UserID) -> list[AccountSchema]:
        async with self.session_factory() as session:
            stmt = select(Accounts).where(Accounts.handler_id == handler_id.value)
            accounts = await session.execute(stmt)
            return [account.convert_to_pydantic_model() for account in accounts.scalars()]

    async def get_total_balance_by_account_id(self, account_id: AccountID) -> float:
        async with self.session_factory() as session:
            stmt = select(Accounts.balance).where(Accounts.id == account_id.value)
            balance = await session.execute(stmt)
            return balance.scalar_one()

    async def increase_balance(
            self,
            value: float,
            account_id: AccountID
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        async with self.session_factory() as session:
            stmt = select(Accounts).where(Accounts.id == account_id.value)
            result = await session.execute(stmt)
            account_for_increase = result.scalar_one()
            account_for_increase.balance += value
            await session.commit()
            return SuccessfulMessageJSON()

    async def decrease_balance(
            self,
            value: float,
            account_id: AccountID
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        async with self.session_factory() as session:
            stmt = select(Accounts).where(Accounts.id == account_id.value)
            result = await session.execute(stmt)
            account_for_decrease = result.scalar_one()
            account_for_decrease.balance -= value
            await session.commit()
            return SuccessfulMessageJSON()


def get_sqlalchemy_postgres_accounts_repository() -> SQLAlchemyPostgresAccountRepository:
    return SQLAlchemyPostgresAccountRepository()
