from uuid import uuid4
from dataclasses import dataclass

from pydantic import EmailStr

from repositories import get_sqlalchemy_postgres_users_repository
from repositories.users.schemas import AddUserSchema, UserID, AddUserFromEndpointsSchema, SuccessfulMessageJSON, \
    UnsuccessfulMessageJSON, UserSchema, PhoneNumber


@dataclass
class UsersService:

    users_repository = get_sqlalchemy_postgres_users_repository()

    @staticmethod
    def _generate_user_id():
        return f"user-{str(uuid4()).replace('-', '')}"

    async def create_user(self, user: AddUserFromEndpointsSchema) -> UserID:
        print(f"Начинаем создание юзера с данными: {user}")
        user_for_add = AddUserSchema(
            id=self._generate_user_id(),
            first_name=user.first_name,
            last_name=user.last_name,
            surname=user.surname,
            email=user.email,
            phone=user.phone,
            date_of_birth=user.date_of_birth
        )
        new_user_id = await self.users_repository.create_user(user=user_for_add)
        print("Создали юзерка, сейчас вернем.")
        return new_user_id

    async def deactivate_user_by_id(self, user_id: UserID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        await self.users_repository.deactivate_user_by_id(user_id=user_id)
        return SuccessfulMessageJSON()

    async def activate_user_by_id(self, user_id: UserID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        await self.users_repository.activate_user_by_id(user_id=user_id)
        return SuccessfulMessageJSON()

    async def get_user_by_id(self, user_id: UserID) -> UserSchema:
        user_as_pydantic_model = await self.users_repository.get_user_by_id(user_id=user_id)
        return user_as_pydantic_model

    async def get_user_by_email(self, email: EmailStr) -> UserSchema:
        user_as_pydantic_model = await self.users_repository.get_user_by_email(email=email)
        return user_as_pydantic_model

    async def get_user_by_phone(self, phone: PhoneNumber) -> UserSchema:
        user_as_pydantic_model = await self.users_repository.get_user_by_phone(phone=phone)
        return user_as_pydantic_model


def get_users_service() -> UsersService:
    return UsersService()


if __name__ == '__main__':
    print(UsersService._generate_user_id())
