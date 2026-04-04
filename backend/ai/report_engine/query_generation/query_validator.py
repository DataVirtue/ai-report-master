from typing import List
from typing import Tuple


class QueryValidator:
    sql_allowed_action_keywords = ["select"]
    sql_action_keywords = [
        # DML (Data Manipulation Language)
        "SELECT",
        "INSERT",
        "UPDATE",
        "DELETE",
        "TRUNCATE",
        # DDL (Data Definition Language)
        "CREATE",
        "ALTER",
        "DROP",
        "RENAME",
        # TCL (Transaction Control Language)
        "COMMIT",
        "ROLLBACK",
        "SAVEPOINT",
        # DCL (Data Control Language)
        "GRANT",
        "REVOKE",
        # Common Clauses and Operators (often used in conjunction with action keywords)
    ]

    def __init__(self, sql_allowed_action_keywords: List[str]) -> None:
        self.allowed_actions = [
            action.lower().strip() for action in sql_allowed_action_keywords
        ]

    def validate_query(self, query) -> Tuple[bool, str]:
        query_words = query.lower().split()
        for word in self.sql_action_keywords:
            # Check if the restricted word is in the query
            # and specifically NOT in your allowed list
            if word in query_words and word not in self.sql_allowed_action_keywords:
                return False, f"'{word}' in query is not allowed in actions"

        return True, ""
