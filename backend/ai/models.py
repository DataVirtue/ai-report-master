from django.db import models
from pgvector.django import VectorField
from django.conf import settings


class Embedding(models.Model):
    content = models.JSONField()
    embedding = VectorField(dimensions=1532)
    metadata = models.JSONField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class Conversation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, default="New Chat")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation, on_delete=models.CASCADE, related_name="messages"
    )
    role = models.CharField(
        max_length=30,
        choices=(
            ("user", "user"),
            ("assistant", "assistant"),
            ("system", "system"),
            ("tool", "tool"),
        ),
    )
    content = models.TextField()
    order = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("conversation", "order")
        ordering = ["order"]
        indexes = [models.Index(fields=["conversation", "order"])]

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.conversation.updated_at = self.created_at
        self.conversation.save(updated_fields=["updated_at"])
