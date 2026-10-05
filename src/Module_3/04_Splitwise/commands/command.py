from abc import ABC, abstractmethod

class Command(ABC):
    @abstractmethod
    def matches(self, input_str: str) -> bool:
        pass

    @abstractmethod
    def execute(self, input_str: str) -> None:
        pass