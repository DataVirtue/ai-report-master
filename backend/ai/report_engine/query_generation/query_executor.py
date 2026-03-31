import logging
from typing import Dict, Tuple, List
from sqlalchemy import text
from sqlalchemy.exc import DBAPIError


class QueryExecutor:
    def __init__(self, db_engine, query_validator):
        self.db_engine = db_engine
        self.query_validator = query_validator

    def execute_query(self, query) -> Tuple[List, bool, str]:
        is_valid, reason = self.query_validator.validate_query(query)
        if not is_valid:
            return [], False, reason

        with self.db_engine.connect() as connection:
            try:
                result_proxy = connection.execute(text(query))
                results = result_proxy.fetchall()
                if results:
                    # Get column names (adjust based on how you get results in your specific setup)
                    # For a ResultProxy, you can access keys (column names)
                    keys = list(result_proxy.keys())

                    # data = {
                    #     key: [row[i] for row in results] for i, key in enumerate(keys)
                    # }
                    data = [dict(zip(keys, row)) for row in results]
                    print("Data", "*" * 100, data)

                    return data, True, ""

            except DBAPIError as e:
                logging.error(f"Could not execute query {e}")
                return [], False, f"Query Failed with error {e}"

        return [], False, "Unknown error"
