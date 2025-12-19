from abc import ABC, abstractmethod


class ASTreeGeneration(ABC):
    @abstractmethod
    def flat_tree(self) -> dict: ...
