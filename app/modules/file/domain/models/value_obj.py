from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Shift:
    start: int
    end: int


@dataclass(frozen=True)
class Position:
    start: int
    end: int
