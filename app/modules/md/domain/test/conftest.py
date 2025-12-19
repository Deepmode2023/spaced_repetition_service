import pytest
from ..token import Token


@pytest.fixture(scope="package")
def postfix_prefix_data() -> tuple[str, str]:
    return "*", "*"


@pytest.fixture()
def token() -> Token:
    return Token(0, 10, "TokenExample", "*", "*")
