from embedding_generator import EmbeddingGenerator
from vector_store import FaissVectorStore
from typing import List


class TableRetriever:
    base_query = "represent this query for retrieving relevant tables: "

    def __init__(self, embedding_generator=None, vector_store=None) -> None:
        self.embedding_generator = embedding_generator or EmbeddingGenerator()
        self.vector_store = vector_store or FaissVectorStore(
            self.embedding_generator.dimension()
        )

    def retrieve_tables(self, query: str, top_k=4) -> List:
        query = query.strip()
        if not query:
            return []
        search_query = self.base_query + query.lower()
        embedded_vector = self.embedding_generator.embed_text(search_query)
        return self.vector_store.search(embedded_vector, top_k)
