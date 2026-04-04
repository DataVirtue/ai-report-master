from abc import ABC, abstractmethod
from typing import List


class VectorStore(ABC):
    @abstractmethod
    def add(self, vector, data):
        pass

    @abstractmethod
    def add_batch(self, vectors, data_list):
        pass

    @abstractmethod
    def search(self, vector) -> List:
        pass
