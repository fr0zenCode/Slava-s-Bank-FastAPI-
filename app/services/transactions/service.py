from dataclasses import dataclass

from repositories.transactions.abstract import AbstractTransactionsRepository
from repositories.transactions.postgres import get_sqlalchemy_postgres_transactions_repository


@dataclass
class TransactionsService:

    transactions_repository: AbstractTransactionsRepository = get_sqlalchemy_postgres_transactions_repository()

    async def registry_transaction_in_system(self):
        ...

    async def finish_transaction(self):
        ...

    async def get_transaction_by_id(self):
        ...

    async def get_all_users_transactions_by_user_id(self):
        ...


def get_transactions_service() -> TransactionsService:
    return TransactionsService()
