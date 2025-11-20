from abc import ABC, abstractmethod


class BaseExceptionExternal(Exception, ABC):
    status: int

    @abstractmethod
    def get_message(self) -> str: ...


class BaseExceptionInternal(Exception, ABC):
    @abstractmethod
    def get_message(self) -> str: ...
