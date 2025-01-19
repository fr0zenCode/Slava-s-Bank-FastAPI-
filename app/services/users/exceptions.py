from dataclasses import dataclass


@dataclass(eq=False)
class InvalidPhoneNumberException(Exception):
    phone_number: str

    @property
    def message(self):
        return f"Invalid phone number: {self.phone_number}. Try again."

    def __str__(self):
        return self.message
