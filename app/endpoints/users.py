from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.users.schemas import AddUserFromEndpointsSchema, UserID, SuccessfulMessageJSON, \
    UnsuccessfulMessageJSON
from services.users.service import UsersService, get_users_service

users_router = APIRouter(prefix="/users", tags=["Users API"])


@users_router.get("/get-user")
async def get_user(user_id: str):
    return {"user-id": user_id}


@users_router.post("/create-user")
async def create_user(
        user: AddUserFromEndpointsSchema,
        users_service: Annotated[UsersService, Depends(get_users_service)]
):
    new_user_id = await users_service.create_user(user=user)
    return {
        "successful": True,
        "created-user-id": new_user_id.value
    }


@users_router.post("/deactivate-user")
async def deactivate_user(
        user_id: UserID,
        users_service: Annotated[UsersService, Depends(get_users_service)]
) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
    json_response_as_pydantic_model = await users_service.deactivate_user_by_id(user_id=user_id)
    return json_response_as_pydantic_model
