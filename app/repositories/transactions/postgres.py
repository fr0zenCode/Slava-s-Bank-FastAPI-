from dataclasses import dataclass

from .abstract import AbstractOperationsRepository


@dataclass
class PostgresOperationsRepository(AbstractOperationsRepository):
    ...
