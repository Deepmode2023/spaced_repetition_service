from typing import Optional
from dataclasses import dataclass
from ..exceptions.base import BaseExceptionExternal, BaseExceptionInternal
from app.infrastucture.db.base import ClassArgument


@dataclass
class SieveValueErrorExceptionExternal(BaseExceptionExternal):
    mandatory_fields: list[str]
    status = 409

    def get_message(self):
        return f"Need to pass the mandatory fields={', '.join(self.mandatory_fields)}"


@dataclass
class SieveValueErrorExceptionInternal(BaseExceptionInternal):
    message: str

    def get_message(self):
        return self.message


def validate_mandatory_field(field: str, kwargs: dict):
    if field not in kwargs:
        raise SieveValueErrorExceptionExternal(mandatory_fields=[field])


def process_field(field: str, kwargs: dict, acc: dict):
    if field in kwargs and kwargs[field] is not None:
        acc[field] = kwargs[field]


def seive_kwargs_by_white_list(
    white_list: list[ClassArgument],
    kwargs: dict[str, any] = None,
    acc: dict[str, any] = None,
) -> dict[str, any]:
    kwargs = kwargs or {}
    acc = acc or {}

    if not isinstance(white_list, list) or any(
        not isinstance(item, ClassArgument) for item in white_list
    ):
        raise TypeError("white_list must contain the list[ClassArgument] type")

    for field, nullable in white_list:
        if not nullable:
            validate_mandatory_field(field, kwargs)
        process_field(field, kwargs, acc)

    return acc


def args_sieve(
    args: list[any],
) -> list[any]:
    """
    Filters a List passed as positional arguments, excluding keys that are `None`.

    Args:
        *args: Positional dictionaries to filter. Only the first list is processed.
    Returns:
        List[Any]: A filtered dictionary.

    Raises:
        ValueError: If no dictionary is provided or the first argument is not a list.
    """

    if isinstance(args, list) or isinstance(args, tuple):
        return [arg for arg in args if arg is not None]

    raise SieveValueErrorExceptionInternal(message="args must be a list or tuple.")


def handle_arguments(
    white_list_keys: Optional[list[str]] = [],
    *args: dict[any, any],
    **kwargs: dict[any, any],
) -> list[list[any], dict[any, any]]:
    return (
        args_sieve(args),
        seive_kwargs_by_white_list(kwargs=kwargs, white_list=white_list_keys),
    )
