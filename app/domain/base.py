from dataclasses import dataclass


@dataclass(frozen=True)
class BaseException(Exception):
    message: str
    status: int

    def get_message(self) -> str:
        return self.message
