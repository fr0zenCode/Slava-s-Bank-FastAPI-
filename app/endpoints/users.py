from typing import Annotated

from fastapi import APIRouter, Depends

from repositories.users.schemas import AddUserFromEndpointsSchema
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
