from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "active"
    DISABLED = "disabled"
    SUSPENDED = "suspended"


class OperationType(Enum):
    WITHDRAW = "withdraw"
    DEPOSIT = "deposit"


class TransactionStatus(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
