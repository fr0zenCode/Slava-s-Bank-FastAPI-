from dataclasses import dataclass
from abc import ABC, abstractmethod

from database.enums import TransactionStatus
from repositories.accounts.schemas import AccountID
from repositories.transactions.schemas import TransactionID, AddTransactionSchema, TransactionSchema
from repositories.users.schemas import SuccessfulMessageJSON, UnsuccessfulMessageJSON


@dataclass
class AbstractTransactionsRepository(ABC):
    @abstractmethod
    async def registry_transaction_in_system(self, transaction: AddTransactionSchema) -> TransactionID:
        ...

    @abstractmethod
    async def get_transaction_by_id(self, transaction_id: TransactionID) -> TransactionSchema:
        ...

    @abstractmethod
    async def change_transaction_status(
            self,
            transaction_id: TransactionID,
            transaction_status: TransactionStatus
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        ...

    @abstractmethod
    async def get_all_users_transactions_by_account_id(self, account_id: AccountID) -> list[TransactionSchema]:
        ...
