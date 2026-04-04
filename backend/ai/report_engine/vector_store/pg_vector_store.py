from sqlalchemy import false
from ai.report_engine.embeddings.embedding_document_generator import EmbeddingDocument
from .vector_store_interface import VectorStore
from ai.models import Embedding
from django.db.models import F
from typing import List
import logging
from pgvector.django import CosineDistance
import json

logger = logging.getLogger(__name__)


class PgVectorStore(VectorStore):
    def add(self, vector, data):
        Embedding.objects.create(
            content=data,
            embedding=vector.tolist(),  # ⚠️ required for pgvector
        )

    def add_batch(self, vectors, data_list):
        objects = []
        for doc, vector in zip(data_list, vectors):
            objects.append(
                Embedding(
                    content=doc,
                    embedding=vector.tolist(),  # ⚠️ required for pgvector
                )
            )

        Embedding.objects.bulk_create(objects)

    def search(
        self,
        vector,
        k: int = 5,
    ) -> List[str]:
        """
        Performs semantic search using cosine distance.
        """
        qs = Embedding.objects.all()

        results = qs.annotate(distance=CosineDistance("embedding", vector)).order_by(
            "distance"
        )[:k]

        return [r.content for r in results]

    def is_store_built(self):
        logger.info(f"Printing embeggins{len(Embedding.objects.all())}")
        if len(Embedding.objects.all()) >= 1:
            logger.info(f"Printing embeggins{Embedding.objects.all()}")
            return True
        return False
