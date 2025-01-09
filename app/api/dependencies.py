from typing import Annotated

from fastapi import Header, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import config
from app.infrastucture.db.session import get_session


async def session() -> AsyncSession:
    async with get_session() as connect:
        return connect


async def auth_marker(auth_marker: Annotated[str, Header()]):
    """
    Exception raised when the authentication marker provided by the client
    does not match the required marker defined in the service configuration.

    Attributes:
        status_code: HTTP status code to return (403 Forbidden).
        detail: Detailed error message to return to the client.
    """

    if auth_marker != config.AUTH_MARKER:
        raise HTTPException(
            detail="Access forbidden: Invalid or missing authentication marker.",
            status_code=403,
        )
