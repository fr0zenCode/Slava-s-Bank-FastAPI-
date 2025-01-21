from typing import Annotated

from fastapi import APIRouter, Depends
from pydantic import EmailStr

from repositories.users.schemas import AddUserFromEndpointsSchema, UserID, SuccessfulMessageJSON, \
    UnsuccessfulMessageJSON, UserSchema, PhoneNumber
from services.users.service import UsersService, get_users_service

users_router = APIRouter(prefix="/users", tags=["Users API"])


@users_router.get("/get-user-by-id")
async def get_user(
        user_id: str,
        users_service: Annotated[UsersService, Depends(get_users_service)]
) -> UserSchema:
    user_as_pydantic_model = await users_service.get_user_by_id(user_id=UserID(value=user_id))
    return user_as_pydantic_model


@users_router.get("/get-user-by-email")
async def get_user_by_email(
        email: EmailStr,
        users_service: Annotated[UsersService, Depends(get_users_service)]
):
    user_as_pydantic_model = await users_service.get_user_by_email(email=email)
    return user_as_pydantic_model


@users_router.get("/get-user-by-phone")
async def get_user_by_phone(
        phone: str,
        users_service: Annotated[UsersService, Depends(get_users_service)]
):
    user_as_pydantic_model = await users_service.get_user_by_phone(phone=PhoneNumber(value=phone))
    return user_as_pydantic_model


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


@users_router.post("/activate-user")
async def activate_user(
        user_id: UserID,
        users_service: Annotated[UsersService, Depends(get_users_service)]
) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
    json_response_as_pydantic_model = await users_service.activate_user_by_id(user_id=user_id)
    return json_response_as_pydantic_model
