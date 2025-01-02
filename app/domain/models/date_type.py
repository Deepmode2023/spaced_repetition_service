from math import floor, log10

import pendulum
from pydantic import ValidationInfo

from ..utils.time import convert_to_timestamp


class DateType:
    date: pendulum.DateTime
    timestamp: int

    def __init__(self, date):
        """
        Initialize DateType from timestamp or ISO date string.
        Raises ValueError for unknown formats.
        """
        if isinstance(date, pendulum.DateTime):
            self.date = date
        elif isinstance(date, (int, float)):
            self.date = self._parse_timestamp_to_date(date)
        elif isinstance(date, str):
            self.date = self._parse_str_to_date(date)
        else:
            raise ValueError("Invalid date format")

        self.timestamp = self.date.int_timestamp

    def __repr__(self):
        return f"DateType(timestamp={self.timestamp}, date={self.date})"

    def __eq__(self, value):
        other_timestamp = self._get_timestamp(value)
        return other_timestamp is not None and self.timestamp == other_timestamp

    def __lt__(self, value):
        other_timestamp = self._get_timestamp(value)
        return other_timestamp is not None and self.timestamp < other_timestamp

    def __gt__(self, value):
        other_timestamp = self._get_timestamp(value)
        return other_timestamp is not None and self.timestamp > other_timestamp

    def _get_timestamp(self, value):
        if isinstance(value, DateType):
            return value.timestamp
        elif isinstance(value, (int, float)):
            return value
        elif hasattr(value, "timestamp") and callable(value.timestamp):
            return value.timestamp()
        return None

    @staticmethod
    def _check_is_timestamp(date):
        """
        Check if the value is a valid numeric timestamp.
        """
        try:
            float(date)
            return True
        except ValueError:
            return False

    @staticmethod
    def _parse_timestamp_to_date(timestamp):
        """
        Parse timestamp of different resolutions into pendulum.DateTime.
        Supports seconds, milliseconds, microseconds, and nanoseconds.
        """
        return pendulum.from_timestamp(convert_to_timestamp(timestamp, 10))

    @classmethod
    def _parse_str_to_date(cls, date: str):
        """
        Check passing date str on pendulum date format
        """
        if isinstance(date, str):
            return pendulum.parse(date)

    @classmethod
    def validate_date_field(cls, date: str | int, _: ValidationInfo):
        """
        Check field on correct string, integer, or pendulum.DateTime type.
        """
        try:
            if isinstance(date, pendulum.DateTime):
                return cls(date)
            if cls._check_is_timestamp(date):
                return cls(cls._parse_timestamp_to_date(date))
            if isinstance(date, str):
                return cls(cls._parse_str_to_date(date))
        except Exception:
            raise ValueError(
                f"Value error, Arguments date={date} is encorrect. "
                "You must pass integer equal 10-19 chars or string with correct date format = year-month-day"
            )
