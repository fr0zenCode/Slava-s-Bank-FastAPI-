import datetime
import uuid
from dataclasses import dataclass, field

from database.enums import TransactionStatus
from repositories.accounts.abstract import AbstractAccountsRepository
from repositories.accounts.postgres import get_sqlalchemy_postgres_accounts_repository
from repositories.accounts.schemas import AccountID
from repositories.transactions.abstract import AbstractTransactionsRepository
from repositories.transactions.postgres import get_sqlalchemy_postgres_transactions_repository
from repositories.transactions.schemas import AddTransactionFromEndpointsSchema, TransactionID, AddTransactionSchema, \
    TransactionSchema
from repositories.users.schemas import SuccessfulMessageJSON, UnsuccessfulMessageJSON


@dataclass
class TransactionsService:

    transactions_repository: AbstractTransactionsRepository = field(
        default_factory=get_sqlalchemy_postgres_transactions_repository
    )
    accounts_repository: AbstractAccountsRepository = field(
        default_factory=get_sqlalchemy_postgres_accounts_repository
    )

    @staticmethod
    def _generate_transaction_id():
        return f"transaction-id-{uuid.uuid4()}"

    async def registry_transaction_in_system(self, transaction: AddTransactionFromEndpointsSchema) -> TransactionID:
        transaction_for_add = AddTransactionSchema(
            id=self._generate_transaction_id(),
            status=TransactionStatus.PENDING,
            transaction_date=datetime.datetime.utcnow(),
            amount=transaction.amount,
            initializer_id=transaction.initializer_id,
            recipient_id=transaction.recipient_id
        )
        new_transaction_id = await self.transactions_repository.registry_transaction_in_system(
            transaction=transaction_for_add
        )
        return new_transaction_id

    async def finish_transaction(
            self,
            transaction_id: TransactionID
    ) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        transaction = await self.get_transaction_by_id(transaction_id=transaction_id)
        response = await self.accounts_repository.decrease_balance(
            value=transaction.amount,
            account_id=AccountID(value=transaction.initializer_id)
        )
        if not isinstance(response, SuccessfulMessageJSON):
            print("Не смогли снять деньги")
            return UnsuccessfulMessageJSON()

        response = await self.accounts_repository.increase_balance(
            value=transaction.amount,
            account_id=AccountID(value=transaction.recipient_id)
        )

        if not isinstance(response, SuccessfulMessageJSON):
            print("Деньги сняли, но не смогли положить")
            return UnsuccessfulMessageJSON()

        await self.transactions_repository.change_transaction_status(
            transaction_id=transaction_id,
            transaction_status=TransactionStatus.COMPLETED
        )

        return SuccessfulMessageJSON()

    async def get_transaction_by_id(self, transaction_id: TransactionID) -> TransactionSchema:
        transaction = await self.transactions_repository.get_transaction_by_id(transaction_id=transaction_id)
        return transaction

    async def get_all_users_transactions_by_account_id(self, account_id: AccountID) -> list[TransactionSchema]:
        transactions = await self.transactions_repository.get_all_users_transactions_by_account_id(
            account_id=account_id
        )
        return transactions


def get_transactions_service() -> TransactionsService:
    return TransactionsService()
