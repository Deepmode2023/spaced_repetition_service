from typing import Annotated

import pendulum
from fastapi import Query
from pydantic_core import core_schema

from app.domain.models import DateType as Date

DESCRIBE_MESSAGE_TYPE = "You must pass 'integer' equal 10-19 chars or 'string' with correct date format = year-month-day hour:min:sec"
OPENAPI_DOCS = {
    "description": DESCRIBE_MESSAGE_TYPE,
    "openapi_examples": [
        {
            "summary": "UNIX Timestamp",
            "description": "You will pass 'integer' equals 10-19 char",
            "value": pendulum.now().int_timestamp,
        },
        {
            "summary": "ISO Format",
            "description": "Time in format YEARS-MONTH-DAY HOUR:MINET:SECOND.MICROSECOND+UTC",
            "value": pendulum.now(),
        },
        {
            "summary": "Another ISO Format",
            "description": "Time in format YEARS-MONTH-DAY",
            "value": pendulum.now().date(),
        },
    ],
}


class DateType(Date):
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type, handler):
        return core_schema.with_info_plain_validator_function(
            cls.validate_date_field, metadata={"type": "string"}
        )

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: core_schema.CoreSchema, handler):
        return {
            "type": "string",
            "description": DESCRIBE_MESSAGE_TYPE,
        }


RequiredQueryDateType = Annotated[
    DateType,
    Query(
        **OPENAPI_DOCS,
    ),
]

OptionalQueryDateType = Annotated[
    DateType,
    Query(
        default_factory=pendulum.now,
        **OPENAPI_DOCS,
    ),
]
