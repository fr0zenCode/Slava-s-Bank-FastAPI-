from dataclasses import dataclass
from datetime import date

from pydantic import EmailStr
from sqlalchemy import insert, update, select

from .abstract import AbstractUsersRepository
from database.models import Users
from database.core import get_sqlalchemy_async_database_helper
from .schemas import AddUserSchema, UserID, SuccessfulMessageJSON, UnsuccessfulMessageJSON, UserSchema, PhoneNumber


@dataclass
class SQLAlchemyPostgresUsersRepository(AbstractUsersRepository):

    database_helper = get_sqlalchemy_async_database_helper()
    session_factory = database_helper.get_session_factory()

    async def create_user(self, user: AddUserSchema) -> UserID:
        async with self.session_factory() as session:
            stmt = insert(Users).values(
                id=user.id,
                first_name=user.first_name,
                last_name=user.last_name,
                surname=user.surname,
                date_of_birth=user.date_of_birth,
                registration_date=date.today(),
                phone=user.phone,
                email=user.email,
                is_active=True
            ).returning(Users.id)
            new_user_id = await session.execute(stmt)
            await session.commit()
            return UserID(value=new_user_id.scalar_one())

    async def deactivate_user_by_id(self, user_id: UserID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        async with self.session_factory() as session:
            stmt = update(Users).values(is_active=False).where(Users.id == user_id.value)
            await session.execute(stmt)
            await session.commit()
            return SuccessfulMessageJSON()

    async def activate_user_by_id(self, user_id: UserID) -> SuccessfulMessageJSON | UnsuccessfulMessageJSON:
        async with self.session_factory() as session:
            stmt = update(Users).values(is_active=True).where(Users.id == user_id.value)
            await session.execute(stmt)
            await session.commit()
            return SuccessfulMessageJSON()

    async def get_user_by_id(self, user_id: UserID) -> UserSchema:
        async with self.session_factory() as session:
            stmt = select(Users).where(Users.id == user_id.value)
            user = await session.execute(stmt)
            user_as_pydantic_model = user.scalar_one().convert_to_pydantic_model()
            return user_as_pydantic_model

    async def get_user_by_email(self, email: EmailStr) -> UserSchema:
        async with self.session_factory() as session:
            stmt = select(Users).where(Users.email == email)
            user = await session.execute(stmt)
            user_as_pydantic_model = user.scalar_one().convert_to_pydantic_model()
            return user_as_pydantic_model

    async def get_user_by_phone(self, phone: PhoneNumber) -> UserSchema:
        async with self.session_factory() as session:
            stmt = select(Users).where(Users.phone == phone.value)
            user = await session.execute(stmt)
            user_as_pydantic_model = user.scalar_one().convert_to_pydantic_model()
            return user_as_pydantic_model


def get_sqlalchemy_postgres_users_repository() -> SQLAlchemyPostgresUsersRepository:
    return SQLAlchemyPostgresUsersRepository()
