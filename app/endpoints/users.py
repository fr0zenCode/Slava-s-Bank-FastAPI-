from fastapi import APIRouter

from app.services.users.schemas import AddUserSchema

users_router = APIRouter(prefix="/users", tags=["Users API"])


@users_router.get("/get-user")
async def get_user(user_id: str):
    return {"user-id": user_id}


@users_router.post("/create-user")
async def create_user(user: AddUserSchema):
    return {"successfully": True,
            "new-user": user}
