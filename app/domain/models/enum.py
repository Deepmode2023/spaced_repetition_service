from abc import ABC, abstractmethod
from enum import Enum


class EnumABC(ABC, Enum):
    @classmethod
    @abstractmethod
    def fields(self): ...

    @property
    @abstractmethod
    def get_name(self): ...
