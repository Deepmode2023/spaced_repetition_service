import asyncio

from fastapi import HTTPException

from app.domain.exceptions import BaseException


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
        if not hasattr(exception, "status") or not hasattr(exception, "message"):
            return BaseException(status=400, message="Unknown critical error")
        return exception

    async def __dispatch_logs(self): ...

    @property
    def response(self):
        raise HTTPException(
            status_code=self.exception.status,
            detail=self.exception.message,
        )
