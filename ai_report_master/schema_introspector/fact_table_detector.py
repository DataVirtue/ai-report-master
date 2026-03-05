from typing import Dict, List
import sys
import numpy as np
import math


class FactTableDetector:
    def get_z_score(self, value: int, mean_val: int, std_val: int) -> float:
        # Handle division by zero if all values are the same
        if std_val == 0:
            return 0.0

        return float((value - mean_val) / std_val)

    def generate_role_hint(
        self, table_stats_list: List, relationship_graph: Dict, **kwargs
    ) -> Dict:
        tipping_score = kwargs.get("tipping_score", 0.0)
        fk_multiplier = kwargs.get("fk_multiplier", 3)
        numeric_multiplier = kwargs.get("numeric_multiplier", 1.5)
        date_multiplier = kwargs.get("date_multiplier", 2)
        text_multipler = kwargs.get("text_multiplier", 2)
        in_degree_multipler = kwargs.get("in_degree_multipler", 1)
        out_degree_multipler = kwargs.get("out_degree_multipler", 2)
        result = {}

        if len(table_stats_list) == 0:
            return result

        min_raw_score = sys.maxsize
        max_raw_score = 0
        score_list_for_stats = []

        for table in table_stats_list:
            table_name = table["table_name"]
            total_column_count = table["total_columns"]
            score = 0
            score += table["foreign_key_column_count"] * fk_multiplier
            score += table["numeric_column_count"] * numeric_multiplier
            score += table["date_column_count"] * date_multiplier
            score -= table["text_column_count"] * text_multipler
            if table["numeric_column_count"] == 0:
                score -= 4
            if table["numeric_column_count"] == 0 and table["date_column_count"] == 0:
                score -= 3
            score -= (
                len(relationship_graph[table_name]["incoming"]) * in_degree_multipler
            )
            score += (
                len(relationship_graph[table_name]["outgoing"]) * out_degree_multipler
            )

            score = (
                score / math.sqrt(total_column_count)
                if math.sqrt(total_column_count) > 0
                else score
            )
            result[table_name] = {
                "raw_fact_score": score,
                "table_role_hint": score > tipping_score,
                "numeric_column_count": table["numeric_column_count"],
                "date_column_count": table["date_column_count"],
                "text_column_count": table["text_column_count"],
                "foreign_key_column_count": table["foreign_key_column_count"],
                "total_columns": total_column_count,
            }
            min_raw_score = min(min_raw_score, score)
            max_raw_score = max(max_raw_score, score)
            score_list_for_stats.append(score)

        array = np.array(score_list_for_stats)
        mean_val = np.mean(array)
        std_val = np.std(array)

        for table in result.keys():
            raw_score = result[table]["raw_fact_score"]
            normalised_score = self.get_z_score(raw_score, mean_val, std_val)
            result[table]["normalized_fact_score"] = normalised_score
            result[table]["table_role_hint"] = "likely a " + (
                "fact table" if normalised_score > 0.0 else "dimension table"
            )

        return result
