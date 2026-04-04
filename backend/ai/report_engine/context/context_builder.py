from typing import Dict
from ai.models import Embedding


class ContextBuilder:
    def __init__(self, embedding_document_dict) -> None:
        self.document_dict = embedding_document_dict

    def get_context(self, query, expanded_tables) -> Dict:
        context = {}
        context["query"] = query
        context["tables"] = expanded_tables
        context_string = ""

        for table in expanded_tables:
            context_string += self.document_dict[table]["embedding_text"]

        context["schema_context"] = context_string

        return context
