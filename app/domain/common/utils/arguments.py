from typing import Optional
from dataclasses import dataclass
from ..exceptions.base import BaseExceptionExternal
from ..models import ClassArgument


@dataclass
class SieveValueErrorExceptionExternal(BaseExceptionExternal):
    mandatory_fields: list[str]
    status = 409

    def get_message(self):
        return f"Need to pass the mandatory fields={', '.join(self.mandatory_fields)}"


def validate_mandatory_field(field: str, kwargs: dict, acc: dict) -> None:
    if field not in kwargs or kwargs[field] is None:
        raise SieveValueErrorExceptionExternal(mandatory_fields=[field])

    acc[field] = kwargs[field]


def process_field(field: str, kwargs: dict, acc: dict) -> None:
    if field in kwargs and kwargs[field] is not None:
        acc[field] = kwargs[field]


def seive_fields(
    required_fields: Optional[tuple[ClassArgument, ...]] = None,
    acc: dict[str, any] = None,
    **kwargs: dict[str, any],
) -> dict[str, any]:
    acc = acc or {}

    if any(not isinstance(item, ClassArgument) for item in required_fields):
        raise TypeError("white_list must contain the tuple[ClassArgument] type")

    for field, nullable in required_fields:
        if not nullable:
            validate_mandatory_field(field, kwargs, acc)
            continue

        process_field(field, kwargs, acc)

    return acc
