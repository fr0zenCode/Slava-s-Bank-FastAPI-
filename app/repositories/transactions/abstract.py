from dataclasses import dataclass
from abc import ABC, abstractmethod

from repositories.transactions.schemas import TransactionID, AddTransactionSchema, TransactionSchema
from repositories.users.schemas import UserID


@dataclass
class AbstractTransactionsRepository(ABC):
    @abstractmethod
    async def registry_transaction_in_system(self, transaction: AddTransactionSchema) -> TransactionID:
        ...

    @abstractmethod
    async def get_transaction_by_id(self, transaction_id: TransactionID) -> TransactionSchema:
        ...

    @abstractmethod
    async def get_all_users_transactions_by_user_id(self, user_id: UserID) -> list[TransactionSchema]:
        ...
