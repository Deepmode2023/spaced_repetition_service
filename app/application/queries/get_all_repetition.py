from sqlalchemy.ext.asyncio import AsyncSession
from app.infrastucture.db.session import get_session

import app.domain.exceptions.external as dom_ex
from app.domain.models import Repetition
from app.domain.models.type import DateType
from app.infrastucture.repositories.sqlalchemy import SQLAlchemyRepetitionRepository

from ..http.exception import HTTPExceptionResponse


async def get_all_repetition(
    start_date: DateType,
    end_date: DateType,
    limit: int,
    offset: int,
) -> list[dict[str, any]]:
    """
    Retrieve all repetitions in the given time interval with a limit on the number and offset.

    This function retrieves repetition data from a database using a repository. The query returns a list of repetitions
    as JSON objects. If an error occurs, the function returns an HTTP response error.

    Args:
        session (AsyncSession): Asynchronous session to communicate with the database.
        start_date (DateType): The start date for filtering repetitions.
        end_date (DateType): The end date for filtering repetitions.
        limit (int): Maximum number of repetitions to return.
        offset (int): The offset for pagination.

    Returns:
        list[dict[str, any]]: A list of dictionaries, where each dictionary represents a JSON-formatted repetition.

    Raises:
        HTTPExceptionResponse: If a `DatabaseError` or `RepetitionNotFoundError` error occurs,
        function returns the corresponding error via HTTPExceptionResponse.
        All other exceptions are also handled via `HTTPExceptionResponse`.

    """
    async with get_session() as session:
        dao = SQLAlchemyRepetitionRepository(session=session)

        try:
            scalar_result: list[Repetition] = await dao.get_all_repetitions(
                start_date=start_date,
                end_date=end_date,
                limit=limit,
                offset=offset,
            )
            print([scalar.to_json for scalar in scalar_result])
            return []
        except dom_ex.DatabaseError as de:
            return HTTPExceptionResponse(exception=de).response
        except dom_ex.RepetitionNotFoundError as rnfe:
            return HTTPExceptionResponse(exception=rnfe).response
        except Exception as ex:
            return HTTPExceptionResponse(exception=ex).response
