from dataclasses import dataclass

from sqlalchemy import insert, select, update, or_

from database.core import get_sqlalchemy_async_database_helper
from database.enums import TransactionStatus
from database.models import Transactions
from .abstract import AbstractTransactionsRepository
from .schemas import AddTransactionSchema, TransactionID, TransactionSchema
from ..accounts.schemas import AccountID
from ..users.schemas import SuccessfulMessageJSON, UnsuccessfulMessageJSON


@dataclass
class PostgresTransactionsRepository(AbstractTransactionsRepository):

    database_helper = get_sqlalchemy_async_database_helper()
    session_factory = database_helper.get_session_factory()

    async def registry_transaction_in_system(self, transaction: AddTransactionSchema) -> TransactionID:
        async with self.session_factory() as session:
            stmt = insert(Transactions).values(
                id=transaction.id,
                amount=transaction.amount,
                initializer_id=transaction.initializer_id,
                recipient_id=transaction.recipient_id,
                status=transaction.status,
                transaction_date=transaction.transaction_date
            ).returning(Transactions.id)
            new_transaction_id = await session.execute(stmt)
            await session.commit()
            return TransactionID(value=new_transaction_id.scalar_one())

    async def get_transaction_by_id(self, transaction_id: TransactionID) -> TransactionSchema:
        async with self.session_factory() as session:
            stmt = select(Transactions).where(Transactions.id == transaction_id.value)
            transaction = await session.execute(stmt)
            return transaction.scalar_one().convert_to_pydantic_model()

    async def change_transaction_status(
            self,
            transaction_id: TransactionID,
            transaction_status: TransactionStatus
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        async with self.session_factory() as session:
            stmt = update(Transactions)\
                .where(Transactions.id == transaction_id.value).values(status=transaction_status)
            await session.execute(stmt)
            await session.commit()
            return SuccessfulMessageJSON()

    async def get_all_users_transactions_by_account_id(self, account_id: AccountID) -> list[TransactionSchema]:
        async with self.session_factory() as session:
            stmt = select(Transactions)\
                .where(or_(Transactions.initializer_id == account_id.value,
                           Transactions.recipient_id == account_id.value))
            transactions = await session.execute(stmt)
            return [transaction.convert_to_pydantic_model() for transaction in transactions.scalars()]


def get_sqlalchemy_postgres_transactions_repository() -> AbstractTransactionsRepository:
    return PostgresTransactionsRepository()
