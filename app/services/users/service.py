from uuid import uuid4
from dataclasses import dataclass


@dataclass
class UsersService:

    @staticmethod
    def _generate_user_id():
        return f"user-{str(uuid4()).replace('-', '')}"

    async def create_user(self):
        ...

    async def deactivate_user(self):
        ...

    async def get_user_by_id(self):
        ...

    async def get_user_by_phone(self):
        ...

    async def get_user_by_email(self):
        ...


if __name__ == '__main__':
    print(UsersService._generate_user_id())
