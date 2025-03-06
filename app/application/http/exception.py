import asyncio

from fastapi import HTTPException

from app.domain.exceptions.base import BaseException


class BaseExceptionUnknown(BaseException):
    def __init__(self, ex: Exception):
        self.status = 400
        self.details = ex

    def get_message(self):
        return f"With details: {self.details}"


class HTTPExceptionResponse:
    exception: BaseException

    def __init__(self, exception: BaseException | Exception):
        self.exception = self._validate_exception(exception=exception)
        asyncio.gather(self.__dispatch_logs())

    def _validate_exception(
        self, exception: BaseException | Exception
    ) -> BaseException:
        """
        Checks for and initializes an exception. If the exception does not have
        required attributes, creates a basic exception with default values.
        """
        if not hasattr(exception, "status"):
            return BaseExceptionUnknown(ex=exception)
        return exception

    async def __dispatch_logs(self): ...

    @property
    def response(self):
        raise HTTPException(
            status_code=self.exception.status,
            detail=self.exception.get_message(),
        )
