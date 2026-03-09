from typing import List
from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:
    # default_model_name = "BAAI/bge-m3"
    default_model_name = "BAAI/bge-small-en"

    def __init__(self, embedding_model=None) -> None:
        if embedding_model:
            self.model = embedding_model
        else:
            self.model = SentenceTransformer(self.default_model_name)

    def embed_text(self, text: str):
        return self.model.encode(text)

    def embed_batch(self, texts: List[str]):
        return self.model.encode(texts)

    def dimension(self) -> int:
        return self.model.get_sentence_embedding_dimension()
