from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class AbstractOperationsRepository(ABC):
    @abstractmethod
    async def registry_transaction(self, from_person, to_person):
        ...

    @abstractmethod
    async def get_transaction_by_id(self):
        ...

    @abstractmethod
    async def get_all_users_transactions_by_user_id(self):
        ...
