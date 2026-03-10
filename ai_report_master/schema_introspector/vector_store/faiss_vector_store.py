from .vector_store_interface import VectorStore
import faiss
import numpy as np


class FaissVectorStore(VectorStore):
    def __init__(self, dim):
        self.index = faiss.IndexFlatIP(dim)
        self.data = []

    def add(self, vector, data):
        vector = np.array([vector]).astype("float32")  # shape (1, dim)
        faiss.normalize_L2(vector)
        self.index.add(vector)
        self.data.append(data)

    def add_batch(self, vectors, data_list):
        vectors = np.array(vectors).astype("float32")
        faiss.normalize_L2(vectors)
        self.index.add(vectors)
        self.data.extend(data_list)

    def search(self, vector, k=4):
        vector = np.array([vector]).astype("float32")  # shape (1, dim)
        distances, indices = self.index.search(vector, k)
        faiss.normalize_L2(vector)

        results = []
        for index in indices[0]:
            if index != -1:
                results.append(self.data[index])
        return results
