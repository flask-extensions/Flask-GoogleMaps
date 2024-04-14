import uuid
from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MarkerContent(ABC):

    def __post_init__(self):
        self.name = f"var_{str(uuid.uuid1())[0:8]}"

    @abstractmethod
    def content(self) -> str:
        pass

    @abstractmethod
    def dom_element(self) -> str:
        pass
