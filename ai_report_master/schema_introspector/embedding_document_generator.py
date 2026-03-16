from typing import List, Dict
from dataclasses import asdict, dataclass


@dataclass
class TableStatistics:
    numeric_column_count: int
    foreign_key_column_count: int
    date_column_count: int
    text_column_count: int
    total_columns: int


@dataclass
class EmbeddingDocument:
    table_name: str
    role: str
    fact_score: float
    columns: List[str]
    relationships: List[str]
    doc_string: str
    statistics: TableStatistics


class EmbeddingDocumentGenerator:
    def render_embedding_text(self, schema: Dict) -> str:
        columns_text = "\n".join(f"- {c}" for c in schema["columns"])

        relationships = schema.get("relationships", [])
        relationships_text = (
            "\n".join(f"- {r}" for r in relationships) if relationships else "- none"
        )

        stats = schema["statistics"]

        return f"""
    Table: {schema["table_name"]}

    Role: {schema["role"]}
    Fact score: {schema["fact_score"]:.2f}

    Columns:
    {columns_text}

    Relationships:
    {relationships_text}

    Doc String:
    {schema["doc_string"]}

    Statistics:
    - numeric columns: {stats["numeric_column_count"]}
    - foreign keys: {stats["foreign_key_column_count"]}
    - date columns: {stats["date_column_count"]}
    - text columns: {stats["text_column_count"]}
    - total columns: {stats["total_columns"]}
    """.strip()

    def generate_embedding_documents(
        self, schema_data: List, fact_table_analysis: Dict, doc_string_dict: Dict
    ) -> List:
        results = []
        for table in schema_data:
            table_name = table["table_name"]
            columns = table["columns"]
            relationships = table["relationships"]

            statistics = TableStatistics(
                numeric_column_count=fact_table_analysis[table_name][
                    "numeric_column_count"
                ],
                date_column_count=fact_table_analysis[table_name]["date_column_count"],
                text_column_count=fact_table_analysis[table_name]["text_column_count"],
                foreign_key_column_count=fact_table_analysis[table_name][
                    "foreign_key_column_count"
                ],
                total_columns=fact_table_analysis[table_name]["total_columns"],
            )
            embedding_document = EmbeddingDocument(
                table_name=table_name,
                role=fact_table_analysis[table_name]["table_role_hint"],
                fact_score=fact_table_analysis[table_name]["normalized_fact_score"],
                columns=[f"{col['name']} ({col['semantic_type']})" for col in columns],
                relationships=[
                    f"references {rel['table_name']}" for rel in relationships
                ],
                doc_string=doc_string_dict[table_name],
                statistics=statistics,
            )
            embedding_text = self.render_embedding_text(asdict(embedding_document))

            results.append(
                {
                    "table_name": table_name,
                    "embedding_text": embedding_text,
                    "metadata": {
                        "fact_score": embedding_document.fact_score,
                        "role_hint": embedding_document.role,
                    },
                }
            )
        return results
