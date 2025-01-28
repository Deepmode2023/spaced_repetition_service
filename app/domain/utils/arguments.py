from typing import Optional

from ..base import BaseException


class SieveValueErrorException(BaseException):
    status: int = 409

    def get_message(self):
        return self.message


def white_list_check_expression(white_list_keys: list[str], key: any) -> bool:
    return key in white_list_keys if len(white_list_keys) > 0 else True


def kwargs_sieve(
    kwargs: dict[any, any] = [],
    white_list_keys: Optional[list[str]] = [],
) -> dict[any, any]:
    """
    Filters keyword arguments, excluding keys that are `None`, unless included in a whitelist.

    Args:
        white_list_key (List[str]): Keys to always include, even if `None`. Default is an empty list.
        **kwargs: Arbitrary keyword arguments to filter.

    Returns:
        Dict[Any, Any]: A filtered dictionary.
    """
    if not isinstance(kwargs, dict):
        raise SieveValueErrorException(message="kwargs must be a dictionary.")

    return {
        key: value
        for key, value in kwargs.items()
        if key is not None
        and white_list_check_expression(white_list_keys=white_list_keys, key=key)
    }


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

    raise SieveValueErrorException("args must be a list or tuple.")


def handle_arguments(
    white_list_keys: Optional[list[str]] = [],
    *args: dict[any, any],
    **kwargs: dict[any, any],
) -> list[list[any], dict[any, any]]:
    return (
        args_sieve(args),
        kwargs_sieve(kwargs, white_list_keys=white_list_keys),
    )
