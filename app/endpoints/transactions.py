from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.accounts.schemas import AccountID
from repositories.transactions.schemas import AddTransactionFromEndpointsSchema, TransactionID, TransactionSchema
from repositories.users.schemas import SuccessfulMessageJSON, UnsuccessfulMessageJSON
from services.transactions.service import TransactionsService, get_transactions_service

transactions_router = APIRouter(prefix="/transactions", tags=["Transactions API"])


@transactions_router.post("/create-transaction")
async def create_transaction(
        transaction: AddTransactionFromEndpointsSchema,
        transactions_service: Annotated[TransactionsService, Depends(get_transactions_service)]
) -> TransactionID:
    new_transaction_id = await transactions_service.registry_transaction_in_system(transaction=transaction)
    return new_transaction_id


@transactions_router.post("/finish-transaction")
async def finish_transaction(
        transaction_id: TransactionID,
        transactions_service: Annotated[TransactionsService, Depends(get_transactions_service)]
) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
    response = await transactions_service.finish_transaction(transaction_id=transaction_id)
    return response


@transactions_router.get("/get-transaction-by-id")
async def get_transaction_by_id(
        transaction_id: str,
        transactions_service: Annotated[TransactionsService, Depends(get_transactions_service)]
) -> TransactionSchema:
    transaction = await transactions_service.get_transaction_by_id(transaction_id=TransactionID(value=transaction_id))
    return transaction


@transactions_router.get("/get-all-accounts-transactions")
async def get_all_accounts_transactions(
        account_id: str,
        transactions_service: Annotated[TransactionsService, Depends(get_transactions_service)]
) -> list[TransactionSchema]:
    transactions = await transactions_service.get_all_users_transactions_by_account_id(
        account_id=AccountID(value=account_id)
    )
    return transactions
