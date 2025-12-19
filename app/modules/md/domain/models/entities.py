from .value_obj import Shift


class Tag:
    def __init__(self, name: str, prefix: str, postfix: str):
        assert isinstance(prefix, str) and isinstance(
            postfix, str
        ), "Please pass the `string` type for prefix and postfix"
        self.name = name
        self.postfix = postfix
        self.prefix = prefix
        self.shift = Shift(len(prefix), len(postfix))

    def __repr__(self):
        return f"Tag(tag='{self.name}', start='{self.shift.start}', end='{self.shift.end}')"

    def __eq__(self, other):
        if isinstance(other, tuple) and len(other) == 2:
            prefix, postfix = other
            return self.prefix.startswith(prefix) and self.postfix.startswith(postfix)

        return False
