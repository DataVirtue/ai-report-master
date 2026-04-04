from django.db import models
from pgvector.django import VectorField


class Embedding(models.Model):
    content = models.JSONField()
    embedding = VectorField(dimensions=1532)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
