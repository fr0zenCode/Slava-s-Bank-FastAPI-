from dataclasses import dataclass
from datetime import date

from sqlalchemy import insert, update

from .abstract import AbstractUsersRepository
from database.models import Users
from database.core import get_sqlalchemy_async_database_helper
from .schemas import AddUserSchema, UserID, SuccessfulMessageJSON, UnsuccessfulMessageJSON


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

    async def get_user_by_id(self):
        ...

    async def get_user_by_email(self):
        ...

    async def get_user_by_phone(self):
        ...


def get_sqlalchemy_postgres_users_repository() -> SQLAlchemyPostgresUsersRepository:
    return SQLAlchemyPostgresUsersRepository()
