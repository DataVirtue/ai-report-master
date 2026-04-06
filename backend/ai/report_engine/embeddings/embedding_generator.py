from typing import List
import numpy
from ai.handlers.open_router_handler import OpenRouterHandler
import logging


class EmbeddingGenerator:
    default_model_name = "BAAI/bge-m3"
    # default_model_name = "BAAI/bge-small-en"

    def __init__(self, embedding_model=None) -> None:
        if embedding_model:
            self.model = embedding_model
        else:
            from sentence_transformers import (
                SentenceTransformer,
            )  # lazy loading transformer

            self.model = SentenceTransformer(self.default_model_name)

    def embed_text(self, text: str):
        return self.model.encode(text)

    def embed_batch(self, texts: List[str]) -> numpy.ndarray:
        return self.model.encode(texts, batch_size=8)

    def dimension(self) -> int | None:
        return self.model.get_sentence_embedding_dimension()


class EmbeddingGeneratorWithOpenRouter(EmbeddingGenerator):
    def __init__(
        self, embedding_model="nvidia/llama-nemotron-embed-vl-1b-v2:free"
    ) -> None:
        self.model = embedding_model
        self.routing_handler = OpenRouterHandler()
        self.dim = None

    def embed_text(self, text: str) -> numpy.ndarray:
        embedding = self.routing_handler.get_embeddings(
            text, self.model, embedding_dimension=1532
        )
        if not self.dim:
            self.dim = len(embedding[0])
        return embedding[0]

    def embed_batch(self, texts: List[str]) -> numpy.ndarray:
        def chunk_list(lst, size):
            for i in range(0, len(lst), size):
                yield lst[i : i + size]

        all_embeddings = []
        count = 0
        total = len(texts)
        size = 5
        for batch in chunk_list(texts, size):
            logging.info(f"{count} of {total} embedding completed")
            embedding = self.routing_handler.get_embeddings(batch, self.model)
            all_embeddings.extend(embedding)
            if not self.dim:
                self.dim = len(embedding[0])
            count += size

        return numpy.vstack(all_embeddings).astype("float32")

    def dimension(self) -> int | None:
        if self.dim is None:
            embedding = self.embed_text("Test text for embedding dimension")
            if not embedding:
                raise Exception("Model did not return an embedding")
            self.dim = len(embedding)
        return self.dim
