from django.core.management.base import BaseCommand
import logging

from ai.report_engine.loader import get_engine

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Build vector store for embeddings"

    def handle(self, *args, **kwargs):
        self.stdout.write("Starting vector store build...")

        engine = get_engine()

        if engine.vector_store.is_store_built():
            self.stdout.write(self.style.SUCCESS("Vector store already exists."))
            return

        self.stdout.write("Building vector store...")

        # You may want to refactor this into a method (better)
        engine.build_vector_store()

        self.stdout.write(self.style.SUCCESS("Vector store built successfully!"))
