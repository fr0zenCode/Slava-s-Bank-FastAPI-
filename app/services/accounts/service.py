from uuid import uuid4
from dataclasses import dataclass


@dataclass
class AccountsService:
    user_id: str

    @staticmethod
    def _generate_account_id() -> str:
        return f"account-{str(uuid4())}"




if __name__ == '__main__':
    print(AccountsService._generate_account_id())
