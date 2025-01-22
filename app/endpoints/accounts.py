from typing import Annotated

from fastapi import APIRouter, Depends

from database.schemas import AccountSchema
from repositories.accounts.schemas import AccountID, AddAccountFromEndpointsSchema, Balance
from repositories.users.schemas import SuccessfulMessageJSON, UnsuccessfulMessageJSON, UserID
from services.accounts.service import AccountsService, get_accounts_service

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts API's"])


@accounts_router.post("/create-account")
async def create_account(
        account: AddAccountFromEndpointsSchema,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> AccountID:
    new_account_id = await accounts_service.create_account(account=account)
    return new_account_id


@accounts_router.post("/deactivate-account")
async def deactivate_account(
        account_id: AccountID,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
    response = await accounts_service.deactivate_account(account_id=account_id)
    return response


@accounts_router.post("/activate-account")
async def activate_account(
        account_id: AccountID,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
    response = await accounts_service.activate_account(account_id=account_id)
    return response


@accounts_router.get("/get-account-by-id")
async def get_account_by_id(
        account_id: str,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> AccountSchema:
    account = await accounts_service.get_account_by_id(account_id=AccountID(value=account_id))
    return account


@accounts_router.get("/get-user-accounts-by-handler-id")
async def get_user_accounts_by_handler_id(
        handler_id: str,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> list[AccountSchema]:
    accounts = await accounts_service.get_user_accounts_by_handler_id(handler_id=UserID(value=handler_id))
    return accounts


@accounts_router.get("/get-total-balance")
async def get_total_balance(
        account_id: str,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> float:
    total_balance = await accounts_service.get_total_balance_by_account_id(account_id=AccountID(value=account_id))
    return total_balance


@accounts_router.post("/increase-balance")
async def increase_balance(
        value: Balance,
        account_id: AccountID,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
    response = await accounts_service.increase_balance(value=value.value, account_id=account_id)
    return response


@accounts_router.post("/decrease-balance")
async def decrease_balance(
        value: Balance,
        account_id: AccountID,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
    response = await accounts_service.decrease_balance(value=value.value, account_id=account_id)
    return response
