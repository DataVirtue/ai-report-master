from abc import ABC, abstractmethod
from typing import List


class VectorStore(ABC):
    @abstractmethod
    def add(self, vector, data):
        pass

    @abstractmethod
    def search(self, vector) -> List:
        pass
