import pendulum
from typing import Union
from ..utils import normalize_timestamp


class DateType:
    __slots__ = ("_dt", "_ts")

    def __init__(self, value: Union[str, int, float, pendulum.DateTime]):
        dt = self._parse(value)
        ts = int(dt.int_timestamp)

        if not isinstance(dt, pendulum.DateTime):
            raise TypeError("Date must be pendulum.DateTime")
        if not isinstance(ts, int):
            raise TypeError("Timestamp must be int")

        self._dt = dt
        self._ts = ts

    @property
    def datetime(self) -> pendulum.DateTime:
        return self._dt

    @property
    def timestamp(self) -> int:
        return self._ts

    def is_before(self, other: "DateType") -> bool:
        return self._ts < other._ts

    def is_after(self, other: "DateType") -> bool:
        return self._ts > other._ts

    def __eq__(self, other) -> bool:
        if not isinstance(other, DateType):
            return NotImplemented
        return self._ts == other._ts

    def __lt__(self, other) -> bool:
        if not isinstance(other, DateType):
            return NotImplemented
        return self._ts < other._ts

    def __repr__(self) -> str:
        return f"DateType(ts={self._ts}, dt={self._dt.to_iso8601_string()})"

    @classmethod
    def _parse(cls, value):
        if isinstance(value, pendulum.DateTime):
            return value

        if isinstance(value, (int, float)):
            return pendulum.from_timestamp(normalize_timestamp(value, 10))

        if isinstance(value, str):
            return pendulum.parse(value)

        raise ValueError(f"Invalid date value: {value!r}")
