from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.accounts.schemas import AccountID, AddAccountFromEndpointsSchema
from services.accounts.service import AccountsService, get_accounts_service

accounts_router = APIRouter(prefix="/accounts", tags=["Accounts API's"])


@accounts_router.post("/create-account")
async def create_account(
        account: AddAccountFromEndpointsSchema,
        accounts_service: Annotated[AccountsService, Depends(get_accounts_service)]
) -> AccountID:
    new_account_id = await accounts_service.create_account(account=account)
    return new_account_id
