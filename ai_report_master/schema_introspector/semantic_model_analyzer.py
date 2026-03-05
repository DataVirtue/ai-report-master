from typing import Dict, List


class SemanticModelAnalyzer:
    def _generate_count_stats(self, columns: List) -> Dict:
        numeric_count = 0
        fk_count = 0
        date_count = 0
        text_count = 0
        for col in columns:
            if col["semantic_type"] == "numeric":
                numeric_count += 1
            if col["semantic_type"] == "datetime":
                date_count += 1
            if col["semantic_type"] == "text":
                text_count += 1
            if col["is_foreign_key"]:
                fk_count += 1

        return {
            "numeric_column_count": numeric_count,
            "date_column_count": date_count,
            "text_column_count": text_count,
            "foreign_key_column_count": fk_count,
            "total_columns": len(columns),
        }

    def generate_table_stats(self, schema_dict: Dict) -> List:
        table_stats_list = []
        schema_data = schema_dict["data"]
        for table_dict in schema_data:
            table_stats_list.append(
                {
                    "table_name": table_dict["table_name"],
                    **self._generate_count_stats(table_dict["columns"]),
                }
            )
        return table_stats_list
