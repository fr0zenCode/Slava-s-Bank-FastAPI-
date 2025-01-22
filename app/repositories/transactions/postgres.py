from dataclasses import dataclass

from sqlalchemy import insert, select

from database.core import get_sqlalchemy_async_database_helper
from database.models import Transactions
from .abstract import AbstractTransactionsRepository
from .schemas import AddTransactionSchema, TransactionID, TransactionSchema
from ..users.schemas import UserID


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
                operation_type=transaction.operation_type,
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

    async def get_all_users_transactions_by_user_id(self, user_id: UserID) -> list[TransactionSchema]:
        async with self.session_factory() as session:
            stmt = select(Transactions)\
                .where(Transactions.initializer_id == user_id.value or Transactions.recipient_id == user_id.value)
            transactions = await session.execute(stmt)
            return [transaction.conver_to_pydantic_model() for transaction in transactions.scalars()]


def get_sqlalchemy_postgres_transactions_repository() -> PostgresTransactionsRepository:
    return PostgresTransactionsRepository()
