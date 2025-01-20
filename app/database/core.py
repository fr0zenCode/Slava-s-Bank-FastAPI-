from dataclasses import dataclass

from sqlalchemy.ext.asyncio import (
    create_async_engine,
    AsyncEngine,
    async_sessionmaker,
    AsyncSession,
)
from sqlalchemy.orm import DeclarativeBase

from config import settings


@dataclass
class SQLAlchemyAsyncDatabaseHelper:
    url: str = str(settings.postgres_url)
    engine: AsyncEngine = create_async_engine(url=url)
    session_factory: async_sessionmaker[AsyncSession] = async_sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
        expire_on_commit=False
    )

    def get_session_factory(self):
        return self.session_factory


class Base(DeclarativeBase):
    ...


def get_sqlalchemy_async_database_helper() -> SQLAlchemyAsyncDatabaseHelper:
    return SQLAlchemyAsyncDatabaseHelper()
