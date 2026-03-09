from .vector_store_interface import VectorStore
import faiss
import numpy as np


class FaissVectorStore(VectorStore):
    def __init__(self, dim):
        self.index = faiss.IndexFlatL2(dim)
        self.data = []

    def add(self, vector, data):
        vector = np.array([vector]).astype("float32")  # shape (1, dim)
        self.index.add(vector)
        self.data.append(data)

    def search(self, vector, k=4):
        vector = np.array([vector]).astype("float32")  # shape (1, dim)
        distances, indices = self.index.search(vector, k)
        results = []
        for index in indices[0]:
            if index != -1:
                results.append(self.data[index])
        return results
